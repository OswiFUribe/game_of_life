import { Component, OnInit, OnDestroy } from '@angular/core';
import { SimulationService, GridResponse } from '../simulation.service';
import { CommonModule } from '@angular/common';
import { interval, Subscription } from 'rxjs';

@Component({
  selector: 'app-grid',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './grid.component.html',
  styleUrls: ['./grid.component.css']
})
export class GridComponent implements OnInit, OnDestroy {
  grid: number[][] = [];
  pollingSubscription!: Subscription;
  private simulationRunning = false;

  constructor(private simulationService: SimulationService) {}

  ngOnInit(): void {
    // Cargar la grilla una vez inicial
    this.loadGrid();
  }

  loadGrid(): void {
    this.simulationService.getGrid().subscribe((data: GridResponse) => {
      this.grid = data.grid;
    });
  }

  onReset(pattern: string = 'glider'): void {
    this.simulationService.resetSimulation(pattern).subscribe((data: GridResponse) => {
      this.grid = data.grid;
    });
    // Si hay un polling activo, puedes detenerlo también al reiniciar
    if (this.pollingSubscription) {
      this.pollingSubscription.unsubscribe();
      this.simulationRunning = false;
    }
  }

  onStep(): void {
    if (this.simulationRunning) {
      this.onPause();
    }
    this.simulationService.stepSimulation().subscribe((data: GridResponse) => {
      this.grid = data.grid;
    });
  }

  onBack(): void {
    if (this.simulationRunning) {
      this.onPause();
    }
    this.simulationService.backSimulation().subscribe((data: GridResponse) => {
      this.grid = data.grid;
    });
  }

   onStart(): void {
    // Llama al endpoint start para que el backend comience su hilo
    this.simulationService.startSimulation().subscribe((data: GridResponse) => {
      this.grid = data.grid;
      // Inicia el polling solo si no está ya en ejecución
      if (!this.simulationRunning) {
        this.simulationRunning = true;
        this.pollingSubscription = interval(1000).subscribe(() => {
          this.loadGrid();
        });
      }
    });
  }

  onPause(): void {
    this.simulationService.pauseSimulation().subscribe((data: GridResponse) => {
      this.grid = data.grid;
      // Detén el polling cuando se pause la simulación
      if (this.pollingSubscription) {
        this.pollingSubscription.unsubscribe();
        this.simulationRunning = false;
      }
    });
  }

  ngOnDestroy(): void {
    // Evita fugas de memoria cancelando el polling cuando el componente se destruye.
    if (this.pollingSubscription) {
      this.pollingSubscription.unsubscribe();
    }
  }
}
