import { Component, output, signal } from '@angular/core';

import { FormsModule } from '@angular/forms';

import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';

@Component({
  selector: 'app-image-upscaler-selection',
  standalone: true,
  imports: [FormsModule, MatFormFieldModule, MatSelectModule],
  templateUrl: './image-upscaler-selection.html',
  styleUrls: ['./image-upscaler-selection.css'],
})
export class ImageUpscalerSelection {
  selectedUpscaler = signal<string | null>(null);
  upscalers = ['convolutional', 'vision-transformer'];
  upscaler = output<string>();

  upscalerChange(fileInputEvent: any) {
    if (this.selectedUpscaler()) {
      this.upscaler.emit(this.selectedUpscaler()!);
    }
  }
}
