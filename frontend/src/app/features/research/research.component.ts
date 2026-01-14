import { Component, OnDestroy, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Subject } from 'rxjs';

import { ResearchService } from '../../core/services/research.service';
import { ButtonComponent } from '../../shared/components/button/button.component';
import { InputComponent } from '../../shared/components/input/input.component';
import { CardComponent } from '../../shared/components/card/card.component';
import { ResultViewerComponent } from '../../shared/components/result-viewer/result-viewer.component';

@Component({
    selector: 'app-research',
    standalone: true,
    imports: [CommonModule, FormsModule, ButtonComponent, InputComponent, CardComponent, ResultViewerComponent],
    template: `
    <div class="research-container">
        <header class="header">
            <h1>Elaia <br>
            Research Platform</h1>
            <p>Powered by Autonomous AI Agents</p>
        </header>

        <section class="search-section">
            <app-card>
                <div class="search-box">
                    <app-input
                        label="Research Topic"
                        placeholder="e.g., The Future of Solar Desalination in 2026"
                        [(value)]="topic"
                        [disabled]="isLoading"
                        (keyup.enter)="startResearch()">
                    </app-input>
                    <div class="actions">
                        <app-button
                            variant="primary"
                            size="lg"
                            [disabled]="!topic || isLoading"
                            (onClick)="startResearch()">
                            {{ isLoading ? 'Researching...' : 'Start Research' }}
                        </app-button>
                    </div>
                </div>
            </app-card>
        </section>

        <section class="logs-section" *ngIf="logs.length > 0 || isLoading">
            <app-card title="Live Agent Logs">
                <div class="logs-container" #logsContainer>
                    <div *ngFor="let log of logs" class="log-entry">
                        <span [innerHTML]="formatLog(log)"></span>
                    </div>
                    <div *ngIf="isLoading" class="loading-indicator">
                        <span class="spinner">⟳</span> Agents are working...
                    </div>
                </div>
            </app-card>
        </section>

        <section class="result-section" *ngIf="result">
            <app-card title="Research Report">
                <app-result-viewer [content]="result"></app-result-viewer>
            </app-card>
        </section>
    </div>
  `,
    styles: [`
    .research-container {
        max-width: 900px;
        margin: 0 auto;
        padding: var(--spacing-xl) var(--spacing-md);
        display: flex;
        flex-direction: column;
        gap: var(--spacing-xl);
    }
    .header {
        text-align: center;
        margin-bottom: var(--spacing-lg);
    }
    .header h1 {
        font-size: 2.5rem;
        margin-bottom: var(--spacing-xs);
        background: linear-gradient(135deg, #818cf8 0%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        letter-spacing: -0.05em;
    }
    .header p {
        color: var(--text-secondary);
        font-size: 1.1rem;
    }
    .search-box {
        display: flex;
        flex-direction: column;
        gap: var(--spacing-lg);
    }
    .actions {
        display: flex;
        justify-content: flex-end;
    }
    .logs-container {
        height: 300px;
        overflow-y: auto;
        background: #0b1120; /* Darker than card */
        padding: var(--spacing-md);
        border-radius: var(--radius-md);
        font-family: 'Fira Code', monospace;
        font-size: 0.9rem;
        display: flex;
        flex-direction: column;
        gap: 0.75rem;
        border: 1px solid var(--border-color);
    }
    .log-entry {
        color: var(--text-secondary);
        border-left: 2px solid var(--border-color);
        padding-left: var(--spacing-sm);
        line-height: 1.5;
        animation: fadeIn 0.3s ease;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(5px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .loading-indicator {
        color: var(--primary);
        font-style: italic;
        margin-top: var(--spacing-sm);
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .spinner {
        animation: spin 1s linear infinite;
        display: inline-block;
    }
    @keyframes spin { 100% { transform: rotate(360deg); } }
    
  `]
})
export class ResearchComponent implements OnDestroy, AfterViewChecked {
    topic = '';
    isLoading = false;
    taskId: string | null = null;
    logs: string[] = [];
    result: string | null = null;

    @ViewChild('logsContainer') private logsContainer!: ElementRef;

    private pollInterval: any;

    constructor(private researchService: ResearchService) { }

    startResearch() {
        if (!this.topic) return;

        this.isLoading = true;
        this.logs = [];
        this.result = null;

        this.researchService.startResearch(this.topic).subscribe({
            next: (res) => {
                this.taskId = res.task_id;
                this.startPolling();
            },
            error: (err) => {
                console.error(err);
                this.isLoading = false;
                this.logs.push("Error starting research.");
            }
        });
    }

    startPolling() {
        if (this.pollInterval) clearInterval(this.pollInterval);

        this.pollInterval = setInterval(() => {
            if (!this.taskId) return;

            this.researchService.getStatus(this.taskId).subscribe({
                next: (status) => {
                    // Determine new logs to append? Or just replace.
                    // Replace is easier but might cause jitter if large.
                    // For now, replacing is robustness.
                    this.logs = status.logs;

                    if (!status.is_running) {
                        this.stopPolling();
                        this.isLoading = false;
                        this.fetchResult();
                    }
                },
                error: (err) => console.error(err)
            });
        }, 2000);
    }

    stopPolling() {
        if (this.pollInterval) {
            clearInterval(this.pollInterval);
            this.pollInterval = null;
        }
    }

    fetchResult() {
        if (!this.taskId) return;
        this.researchService.getResult(this.taskId).subscribe(res => {
            this.result = res.result;
        });
    }

    formatLog(log: string): string {
        return log.replace(/\*\*(.*?)\*\*/g, '<strong class="text-primary-400">$1</strong>');
    }

    ngAfterViewChecked() {
        this.scrollToBottom();
    }

    scrollToBottom(): void {
        if (this.logsContainer) {
            try {
                this.logsContainer.nativeElement.scrollTop = this.logsContainer.nativeElement.scrollHeight;
            } catch (err) { }
        }
    }

    ngOnDestroy() {
        this.stopPolling();
    }
}
