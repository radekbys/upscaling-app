import { Component, output } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-image-select-button',
  standalone: true,
  imports: [MatButtonModule],
  templateUrl: './image-select-button.html',
  styleUrls: ['./image-select-button.css'],
})
export class ImageSelectButton {
  image = output<File>();

  pngInputChange(fileInputEvent: any) {
    if (fileInputEvent.target.files[0]) {
      this.image.emit(fileInputEvent.target.files[0]);
    }
  }
}
