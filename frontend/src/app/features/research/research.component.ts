import {
  Component,
  OnDestroy,
  ViewChild,
  ElementRef,
  AfterViewChecked
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { ResearchService } from '../../core/services/research.service';
import { ButtonComponent } from '../../shared/components/button/button.component';
import { InputComponent } from '../../shared/components/input/input.component';
import { CardComponent } from '../../shared/components/card/card.component';
import { ResultViewerComponent } from '../../shared/components/result-viewer/result-viewer.component';

@Component({
  selector: 'app-research',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    ButtonComponent,
    InputComponent,
    CardComponent,
    ResultViewerComponent
  ],
  template: `
    <div class="ui-container ui-stack">

      <header class="ui-stack ui-center-text ui-glass">
        <h1 class="ui-title">
          Elaia <br />
          Research Platform
        </h1>
        <p class="ui-subtitle">
          Powered by Autonomous AI Agents
        </p>
      </header>

      <section>
        <app-card>
          <div class="ui-stack">
            <app-input
              label="Research Topic"
              placeholder="e.g., The Future of Solar Desalination in 2026"
              [(value)]="topic"
              [disabled]="isLoading"
              (keyup.enter)="startResearch()"
            />

            <div class="ui-row ui-end">
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

      <section *ngIf="logs.length > 0 || isLoading">
        <app-card title="Live Agent Logs">
          <div class="ui-log-panel" #logsContainer>
            <div *ngFor="let log of logs" class="ui-log-entry">
              <span [innerHTML]="formatLog(log)"></span>
            </div>

            <div *ngIf="isLoading" class="ui-log-loading">
              <span class="ui-spinner">⟳</span>
              Agents are working...
            </div>
          </div>
        </app-card>
      </section>

      <section *ngIf="result">
        <app-card title="Research Report">
          <app-result-viewer [content]="result" />
        </app-card>
      </section>

    </div>
  `,
  styles: [`
    :host {
      display: block;
    }
      header{
      gap: 1rem;
      padding: 0;
      }
  `]
})
export class ResearchComponent implements OnDestroy, AfterViewChecked {
  topic = '';
  isLoading = false;
  taskId: string | null = null;
  logs: string[] = [];
  result: string | null = `# Mock Research Report
## Executive Summary
This is a **mock result** to verify the UI component.

- Key finding 1
- Key finding 2

### Analysis
The market is growing...`;

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
      error: () => {
        this.isLoading = false;
        this.logs.push('Error starting research.');
      }
    });
  }

  startPolling() {
    this.stopPolling();

    this.pollInterval = setInterval(() => {
      if (!this.taskId) return;

      this.researchService.getStatus(this.taskId).subscribe(status => {
        this.logs = status.logs;

        if (!status.is_running) {
          this.stopPolling();
          this.isLoading = false;
          this.fetchResult();
        }
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
    return log.replace(
      /\*\*(.*?)\*\*/g,
      '<strong class="ui-text-accent">$1</strong>'
    );
  }

  ngAfterViewChecked() {
    if (this.logsContainer) {
      this.logsContainer.nativeElement.scrollTop =
        this.logsContainer.nativeElement.scrollHeight;
    }
  }

  ngOnDestroy() {
    this.stopPolling();
  }
}
