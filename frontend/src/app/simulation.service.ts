import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface GridResponse {
  grid: number[][];
}

@Injectable({
  providedIn: 'root'
})
export class SimulationService {
  private apiUrl = 'http://localhost:8000';  // URL de tu API backend

  constructor(private http: HttpClient) { }

  getGrid(): Observable<GridResponse> {
    return this.http.get<GridResponse>(`${this.apiUrl}/grid`);
  }

  resetSimulation(pattern: string = 'glider'): Observable<GridResponse> {
    // Puedes enviar el patrón mediante un parámetro query o adaptarlo según tu backend
    return this.http.post<GridResponse>(`${this.apiUrl}/reset?pattern=${pattern}`, {});
  }

  stepSimulation(): Observable<GridResponse> {
    return this.http.post<GridResponse>(`${this.apiUrl}/step`, {});
  }

  backSimulation(): Observable<GridResponse> {
    return this.http.post<GridResponse>(`${this.apiUrl}/back`, {});
  }

  startSimulation(): Observable<GridResponse> {
    return this.http.post<GridResponse>(`${this.apiUrl}/start`, {});
  }

  pauseSimulation(): Observable<GridResponse> {
    return this.http.post<GridResponse>(`${this.apiUrl}/pause`, {});
  }

  setCustomGrid(grid: number[][]): Observable<GridResponse> {
    return this.http.post<GridResponse>(`${this.apiUrl}/grid`, { grid });
  }
}
