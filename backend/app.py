from fastapi import FastAPI
from pydantic import BaseModel
from simulation import create_initial_grid, get_next_state

# Configuración inicial
GRID_ROWS = 20
GRID_COLS = 40

# Inicializa la grilla globalmente
grid = create_initial_grid(GRID_ROWS, GRID_COLS)

# Modelo Pydantic para el estado de la grilla
class GridModel(BaseModel):
    grid: list[list[int]]

app = FastAPI(title="Juego de la Vida API")

@app.get("/grid", response_model=GridModel)
def get_grid():
    """
    Devuelve el estado actual de la grilla.
    """
    return {"grid": grid}

@app.post("/step", response_model=GridModel)
def step_simulation():
    """
    Calcula y devuelve el siguiente estado de la grilla.
    """
    global grid
    grid = get_next_state(grid)
    return {"grid": grid}

@app.post("/reset", response_model=GridModel)
def reset_simulation():
    """
    Reinicia la simulación a la configuración inicial.
    """
    global grid
    grid = create_initial_grid(GRID_ROWS, GRID_COLS)
    return {"grid": grid}
