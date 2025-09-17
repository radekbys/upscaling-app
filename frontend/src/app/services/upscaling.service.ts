import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root',
})
export class UpscalingService {
  private apiUrl = 'http://127.0.0.1:8000/api/upscaling'; // Django backend

  constructor(private http: HttpClient) {}

  convUpscale(image: File) {
    const formData = new FormData();
    formData.append('image', image);

    return this.http.post(`${this.apiUrl}/conv_upscaling/`, formData, {
      responseType: 'blob', // important because backend returns an image
    });
  }

  transUpscale(image: File) {
    const formData = new FormData();
    formData.append('image', image);

    return this.http.post(`${this.apiUrl}/trans_upscaling/`, formData, {
      responseType: 'blob',
    });
  }
}
