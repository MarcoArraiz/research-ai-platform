import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { BackgroundNodes } from './shared/components/background-nodes/background-nodes';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, BackgroundNodes],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('frontend');
}
