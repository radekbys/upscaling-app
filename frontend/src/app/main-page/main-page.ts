import { Component, signal, computed, effect } from '@angular/core';

import { ImageUpscalerSelection } from './image-upscaler-selection/image-upscaler-selection';
import { UpscalingService } from '../services/upscaling.service';
import { ImageSelectButton } from './image-select-button/image-select-button';
import { ImageDownloadButton } from './image-download-button/image-download-button';

@Component({
  selector: 'app-main-page',
  standalone: true,
  imports: [ImageUpscalerSelection, ImageSelectButton, ImageDownloadButton],
  templateUrl: './main-page.html',
  styleUrl: './main-page.css',
})
export class MainPage {
  selectedFile = signal<File | null>(null);
  upscaledImage = signal<Blob | null>(null);
  selectedUpscaler = signal<string | null>(null);
  errorMessage = signal<string | null>(null);

  imagePreviewUrl = computed(() => {
    const file = this.selectedFile();
    if (!file) return null;
    return URL.createObjectURL(file);
  });

  upscaledImageUrl = computed(() => {
    const blob = this.upscaledImage();
    if (!blob) return null;
    return URL.createObjectURL(blob);
  });

  constructor(private upscalingService: UpscalingService) {}

  onUpscalerSelected(upscaler: string) {
    this.selectedUpscaler.set(upscaler);
  }
  onFileSelected(file: File) {
    this.selectedFile.set(file);
  }

  effect = effect(() => {
    const upscaler = this.selectedUpscaler();
    const file = this.selectedFile();

    if (!upscaler || !file) {
      this.upscaledImage.set(null);
      return;
    }

    if (upscaler === 'convolutional') {
      this.upscalingService.convUpscale(file).subscribe({
        next: (blob) => this.upscaledImage.set(blob),
        error: (err) => {
          this.errorMessage.set(`Error: ${err.name} status: ${err.status}`);
        },
      });
    }

    if (upscaler === 'vision-transformer') {
      this.upscalingService.transUpscale(file).subscribe({
        next: (blob) => this.upscaledImage.set(blob),
        error: (err) => {
          this.errorMessage.set(`Error: ${err.name} status: ${err.status} \n`);
        },
      });
    }
  });
}
