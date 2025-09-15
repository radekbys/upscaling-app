import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ImageUpscalerSelection } from '../image-upscaler-selection/image-upscaler-selection';
import { MatToolbarModule } from '@angular/material/toolbar';

@Component({
  selector: 'app-main-page',
  standalone: true,
  imports: [ImageUpscalerSelection, CommonModule, MatToolbarModule],
  templateUrl: './main-page.html',
  styleUrl: './main-page.css',
})
export class MainPage {
  selectedFile: File | null = null;
  selectedUpscaler: string | null = null;
  imagePreviewUrl: string | null = null;

  // handler for file event
  onFileSelected(file: File) {
    this.selectedFile = file;

    // revoke old object URL if present
    if (this.imagePreviewUrl) {
      URL.revokeObjectURL(this.imagePreviewUrl);
    }

    // create new object URL for preview
    this.imagePreviewUrl = URL.createObjectURL(file);
    console.log('Preview URL created:', this.imagePreviewUrl);
  }

  // handler for upscaler event
  onUpscalerSelected(upscaler: string) {
    this.selectedUpscaler = upscaler;
    console.log('Received upscaler:', upscaler);
  }
}
