import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ImageUpscalerSelection } from '../image-upscaler-selection/image-upscaler-selection';

@Component({
  selector: 'app-main-page',
  standalone: true,
  imports: [CommonModule, ImageUpscalerSelection],
  templateUrl: './main-page.html',
  styleUrl: './main-page.css',
})
export class MainPage {}
