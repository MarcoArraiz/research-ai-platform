import { Component, Input, ViewEncapsulation } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MarkdownModule } from 'ngx-markdown';

@Component({
    selector: 'app-result-viewer',
    standalone: true,
    imports: [CommonModule, MarkdownModule],
    template: `
    <div class="result-viewer">
       <markdown [data]="content"></markdown>
    </div>
  `,
    styles: [`
    .result-viewer {
      color: var(--text-primary);
      line-height: 1.7;
      font-size: 1rem;
    }
    
    /* We use ::ng-deep because markdown content is injected dynamically */
    :host ::ng-deep h1, :host ::ng-deep h2, :host ::ng-deep h3 {
      color: var(--primary-hover);
      margin-top: 1.5em;
      margin-bottom: 0.5em;
    }
    
    :host ::ng-deep h1 { font-size: 2em; border-bottom: 1px solid var(--border-color); padding-bottom: 0.3em; }
    :host ::ng-deep h2 { font-size: 1.5em; }
    :host ::ng-deep h3 { font-size: 1.25em; }
    
    :host ::ng-deep p { margin-bottom: 1em; }
    
    :host ::ng-deep ul, :host ::ng-deep ol { margin-bottom: 1em; padding-left: 1.5em; }
    :host ::ng-deep li { margin-bottom: 0.25em; }
    
    :host ::ng-deep strong { color: var(--primary); }
    
    :host ::ng-deep code {
      background-color: var(--bg-input);
      padding: 0.2em 0.4em;
      border-radius: 4px;
      font-family: 'Fira Code', monospace;
      font-size: 0.9em;
    }
    
    :host ::ng-deep pre {
      background-color: #000;
      padding: 1em;
      border-radius: 8px;
      overflow-x: auto;
      margin-bottom: 1em;
    }
    
    :host ::ng-deep pre code {
      background-color: transparent;
      padding: 0;
      color: #e2e8f0;
    }
    
    :host ::ng-deep blockquote {
        border-left: 4px solid var(--primary);
        padding-left: 1rem;
        margin-left: 0;
        color: var(--text-muted);
        font-style: italic;
    }
    
    :host ::ng-deep a {
        color: var(--primary);
        text-decoration: underline;
    }
  `],
    encapsulation: ViewEncapsulation.None
})
export class ResultViewerComponent {
    @Input() content: string = '';
}
