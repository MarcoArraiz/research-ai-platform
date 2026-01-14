import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
    selector: 'app-input',
    standalone: true,
    imports: [CommonModule, FormsModule],
    template: `
    <div class="input-container">
      <label *ngIf="label" [for]="id">{{ label }}</label>
      <input
        [id]="id"
        [type]="type"
        [placeholder]="placeholder"
        [ngModel]="value"
        (ngModelChange)="onValueChange($event)"
        [disabled]="disabled"
      />
    </div>
  `,
    styles: [`
    .input-container {
      display: flex;
      flex-direction: column;
      gap: var(--spacing-xs);
      width: 100%;
    }
    label {
      font-size: 0.875rem;
      font-weight: 500;
      color: var(--text-secondary);
      margin-left: 0.25rem;
    }
    input {
      background-color: var(--bg-input);
      border: 1px solid var(--border-color);
      color: var(--text-primary);
      padding: 0.75rem 1rem;
      border-radius: var(--radius-md);
      font-family: inherit;
      font-size: 1rem;
      transition: all 0.2s ease;
      width: 100%;
      box-sizing: border-box;
    }
    input:focus {
      outline: none;
      border-color: var(--border-focus);
      box-shadow: 0 0 0 4px rgba(129, 140, 248, 0.15);
      background-color: #3b4d66; /* Slightly lighter than bg-input */
    }
    input::placeholder {
      color: var(--text-muted);
    }
    input:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
  `]
})
export class InputComponent {
    @Input() id = `input-${Math.random().toString(36).substr(2, 9)}`;
    @Input() label = '';
    @Input() type = 'text';
    @Input() placeholder = '';
    @Input() value = '';
    @Input() disabled = false;
    @Output() valueChange = new EventEmitter<string>();

    onValueChange(val: string) {
        this.value = val;
        this.valueChange.emit(val);
    }
}
