import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-card',
    standalone: true,
    imports: [CommonModule],
    template: `
    <div class="card">
        <div class="card-header" *ngIf="title">
            <h3 class="card-title">{{ title }}</h3>
        </div>
        <div class="card-content">
            <ng-content></ng-content>
        </div>
    </div>
  `,
    styles: [`
    .card {
      background-color: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-lg);
      box-shadow: var(--shadow-sm);
      overflow: hidden;
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .card:hover {
        box-shadow: var(--shadow-md);
    }
    .card-header {
      padding: var(--spacing-lg) var(--spacing-lg) var(--spacing-md);
    }
    .card-title {
        margin: 0;
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--text-primary);
    }
    .card-content {
      padding: var(--spacing-lg);
    }
  `]
})
export class CardComponent {
    @Input() title = '';
}
