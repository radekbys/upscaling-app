import { Component, input } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-image-download-button',
  imports: [MatButtonModule],
  templateUrl: './image-download-button.html',
  styleUrl: './image-download-button.css',
})
export class ImageDownloadButton {
  upscaledImageUrl = input.required<null | string>();

  downloadBlob(url: null | string, name: string) {
    if (!url) return;

    const a = document.createElement('a');
    a.href = url;
    a.download = name;
    a.click();
  }
}
