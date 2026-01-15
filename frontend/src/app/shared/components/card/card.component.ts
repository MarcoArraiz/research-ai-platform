import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-card',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div [class]="classes">
      <div class="ui-card-header" *ngIf="title">
        <h3 class="ui-card-title">{{ title }}</h3>
      </div>

      <div class="ui-card-content">
        <ng-content></ng-content>
      </div>
    </div>
  `,
  styles: [`
    :host {
      display: block;
    }
  `]
})
export class CardComponent {
  @Input() title = '';
  @Input() variant: 'default' | 'dark' = 'default';

  get classes(): string {
    return [
      'ui-card',
      this.variant === 'dark' ? 'ui-card-dark' : 'ui-card-default'
    ].join(' ');
  }
}
