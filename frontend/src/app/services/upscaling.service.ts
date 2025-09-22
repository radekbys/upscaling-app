import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../environments/environment';

@Injectable({
  providedIn: 'root',
})
export class UpscalingService {
  private apiUrl = environment.apiUrl; // Django backend

  constructor(private http: HttpClient) {}

  convUpscale(image: File) {
    const formData = new FormData();
    formData.append('image', image);

    return this.http.post(`${this.apiUrl}/upscaling/conv_upscaling/`, formData, {
      responseType: 'blob', // important because backend returns an image
    });
  }

  transUpscale(image: File) {
    const formData = new FormData();
    formData.append('image', image);

    return this.http.post(`${this.apiUrl}/upscaling/trans_upscaling/`, formData, {
      responseType: 'blob',
    });
  }
}
