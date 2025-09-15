import { Component, signal } from '@angular/core';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MainPage } from './main-page/main-page';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [MainPage, MatToolbarModule],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  protected readonly title = signal('frontend');
}
