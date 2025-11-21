import { Component, signal } from '@angular/core';

import { MainPage } from './main-page/main-page';
import { Header } from './header/header';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [MainPage, Header],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App {
  protected readonly title = signal('frontend');
}
