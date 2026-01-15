import { Component, Input, Output, EventEmitter } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-input',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="ui-field">
      <label *ngIf="label" class="ui-label" [for]="id">
        {{ label }}
      </label>

      <input
        class="ui-input"
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
    :host {
      display: block;
      width: 100%;
    }
  `]
})
export class InputComponent {
  @Input() id = `input-${Math.random().toString(36).slice(2)}`;
  @Input() label = '';
  @Input() type = 'text';
  @Input() placeholder = '';
  @Input() value = '';
  @Input() disabled = false;

  @Output() valueChange = new EventEmitter<string>();

  onValueChange(value: string) {
    this.value = value;
    this.valueChange.emit(value);
  }
}
