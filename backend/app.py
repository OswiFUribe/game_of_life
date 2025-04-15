from fastapi import FastAPI
from pydantic import BaseModel
import threading
import time
from fastapi.middleware.cors import CORSMiddleware
from simulation import create_initial_grid, get_next_state

# Configuración del grid y tiempo de paso
GRID_ROWS = 20
GRID_COLS = 40
STEP_DELAY = 1  # segundos entre pasos en modo automático

# Variables globales para estado, historial y control de ejecución
grid = create_initial_grid(GRID_ROWS, GRID_COLS, pattern="glider")
history = []  # Para almacenar estados anteriores y permitir retroceder
is_running = False  # Bandera para ejecución automática
simulation_thread = None  # Hilo de simulación automática

def auto_run_simulation():
    """Función que se ejecuta en un hilo en modo automático."""
    global grid, is_running, history
    while is_running:
        # Guardar el estado actual antes de avanzar
        history.append([row[:] for row in grid])
        grid = get_next_state(grid)
        time.sleep(STEP_DELAY)

# Modelo Pydantic para el estado de la grilla
class GridModel(BaseModel):
    grid: list[list[int]]

app = FastAPI(title="Juego de la Vida API")

# Configuración de CORS: permite peticiones de cualquier origen (puedes restringirlo a dominios específicos)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # o especifica [ "http://localhost:4200" ] si solo quieres permitir tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/grid", response_model=GridModel)
def get_grid():
    """
    Devuelve el estado actual de la grilla.
    """
    return {"grid": grid}

@app.post("/grid", response_model=GridModel)
def set_grid(new_grid: GridModel):
    """
    Permite definir una grilla personalizada.
    
    Se envía un JSON con el formato: {"grid": [[0,1,...], [...], ...]}
    """
    global grid, history
    grid = new_grid.grid
    history = []  # Se reinicia el historial
    return {"grid": grid}

@app.post("/reset", response_model=GridModel)
def reset_simulation(pattern: str = "glider"):
    """
    Reinicia la simulación usando un patrón dado, por ejemplo "glider" o "blinker".
    """
    global grid, history
    grid = create_initial_grid(GRID_ROWS, GRID_COLS, pattern=pattern)
    history = []
    return {"grid": grid}

@app.post("/step", response_model=GridModel)
def step_simulation():
    """
    Avanza la simulación un paso.
    Guarda el estado actual en el historial para permitir retroceder.
    """
    global grid, history
    history.append([row[:] for row in grid])
    grid = get_next_state(grid)
    return {"grid": grid}

@app.post("/back", response_model=GridModel)
def back_simulation():
    """
    Retrocede la simulación al estado anterior (si el historial no está vacío).
    """
    global grid, history
    if history:
        grid = history.pop()
    return {"grid": grid}

@app.post("/start", response_model=GridModel)
def start_simulation():
    """
    Inicia la ejecución automática de la simulación.
    Se ejecuta en un hilo que avanza el estado cada STEP_DELAY segundos.
    """
    global is_running, simulation_thread
    if not is_running:
        is_running = True
        simulation_thread = threading.Thread(target=auto_run_simulation, daemon=True)
        simulation_thread.start()
    return {"grid": grid}

@app.post("/pause", response_model=GridModel)
def pause_simulation():
    """
    Pausa la ejecución automática de la simulación.
    """
    global is_running, simulation_thread
    is_running = False
    if simulation_thread:
        simulation_thread.join(timeout=STEP_DELAY + 0.5)
    return {"grid": grid}