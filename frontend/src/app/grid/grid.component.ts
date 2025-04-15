import { Component, OnInit } from '@angular/core';
import { SimulationService, GridResponse } from '../simulation.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-grid',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './grid.component.html',
  styleUrls: ['./grid.component.css']
})
export class GridComponent implements OnInit {
  grid: number[][] = [];

  constructor(private simulationService: SimulationService) {}

  ngOnInit(): void {
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
  }

  onStep(): void {
    this.simulationService.stepSimulation().subscribe((data: GridResponse) => {
      this.grid = data.grid;
    });
  }

  onBack(): void {
    this.simulationService.backSimulation().subscribe((data: GridResponse) => {
      this.grid = data.grid;
    });
  }

  onStart(): void {
    this.simulationService.startSimulation().subscribe((data: GridResponse) => {
      this.grid = data.grid;
    });
  }

  onPause(): void {
    this.simulationService.pauseSimulation().subscribe((data: GridResponse) => {
      this.grid = data.grid;
    });
  }
}
