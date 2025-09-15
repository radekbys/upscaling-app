import { Component, output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-image-upscaler-selection',
  standalone: true,
  imports: [CommonModule, FormsModule, MatFormFieldModule, MatSelectModule, MatButtonModule],
  templateUrl: './image-upscaler-selection.html',
  styleUrls: ['./image-upscaler-selection.css'],
})
export class ImageUpscalerSelection {
  selectedUpscaler: string | null = null;
  upscalers = ['convolutional', 'vision-transformer'];
  image = output<File>();
  upscaler = output<String>();

  pngInputChange(fileInputEvent: any) {
    console.log(fileInputEvent.target.files[0]);
    if (fileInputEvent.target.files[0] && !this.selectedUpscaler) {
      this.image.emit(fileInputEvent.target.files[0]);
      this.upscaler.emit(this.selectedUpscaler ?? 'convolutional');
    }
  }
}
