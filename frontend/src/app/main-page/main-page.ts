import { Component } from '@angular/core';
import { ImageUpscalerSelection } from '../image-upscaler-selection/image-upscaler-selection';

@Component({
  selector: 'app-main-page',
  standalone: true,
  imports: [ImageUpscalerSelection],
  templateUrl: './main-page.html',
  styleUrl: './main-page.css',
})
export class MainPage {}
