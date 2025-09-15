import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-image-upscaler-selection',
  standalone: true,
  imports: [
    CommonModule,
    FormsModule,
    ReactiveFormsModule,
    MatFormFieldModule,
    MatSelectModule,
    MatButtonModule,
  ],
  templateUrl: './image-upscaler-selection.html',
  styleUrls: ['./image-upscaler-selection.css'],
})
export class ImageUpscalerSelection {
  selectedUpscaler: string | null = null;
  upscalers = ['convolutional', 'vision-transformer'];

  pngInputChange(fileInputEvent: any) {
    console.log(fileInputEvent.target.files[0]);
  }
}
