import { Component, Input, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MarkdownModule } from 'ngx-markdown';

@Component({
  selector: 'app-result-viewer',
  standalone: true,
  imports: [CommonModule, MarkdownModule],
  template: `
    <div class="ui-markdown">
      <markdown [data]="content"></markdown>
    </div>
  `,
  styles: [`
    :host {
      display: block;
    }
  `],
  encapsulation: ViewEncapsulation.None
})
export class ResultViewerComponent {
  @Input() content = '';
}
