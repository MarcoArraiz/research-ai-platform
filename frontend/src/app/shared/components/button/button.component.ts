import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-button',
    standalone: true,
    imports: [CommonModule],
    template: `
    <button
      [type]="type"
      [class]="classes"
      [disabled]="disabled"
      (click)="onClick.emit($event)">
      <ng-content></ng-content>
    </button>
  `,
    styles: [`
    button {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      border: 1px solid transparent;
      font-weight: 600;
      transition: all 0.2s ease-in-out;
      cursor: pointer;
      font-family: inherit;
      outline: none;
    }
    button:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
    button:focus-visible {
      box-shadow: 0 0 0 2px var(--border-focus);
    }
    /* Variants */
    .primary {
      background-color: var(--primary);
      color: var(--primary-content);
      box-shadow: var(--shadow-sm);
    }
    .primary:hover:not(:disabled) {
      background-color: var(--primary-hover);
      box-shadow: var(--shadow-md);
      transform: translateY(-1px);
    }
    .primary:active:not(:disabled) {
      transform: translateY(0);
    }
    .secondary {
      background-color: transparent;
      color: var(--text-primary);
      border-color: var(--border-color);
    }
    .secondary:hover:not(:disabled) {
      background-color: var(--bg-input);
      border-color: var(--text-muted);
    }
    /* Sizes */
    .sm { padding: 0.35rem 0.75rem; font-size: 0.875rem; border-radius: var(--radius-sm); }
    .md { padding: 0.6rem 1.25rem; font-size: 1rem; border-radius: var(--radius-md); }
    .lg { padding: 0.85rem 1.75rem; font-size: 1.125rem; border-radius: var(--radius-lg); }
  `]
})
export class ButtonComponent {
    @Input() type: 'button' | 'submit' | 'reset' = 'button';
    @Input() variant: 'primary' | 'secondary' = 'primary';
    @Input() size: 'sm' | 'md' | 'lg' = 'md';
    @Input() disabled = false;
    @Output() onClick = new EventEmitter<Event>();

    get classes(): string {
        return `${this.variant} ${this.size}`;
    }
}
