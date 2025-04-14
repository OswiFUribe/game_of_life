# test_app.py
from fastapi.testclient import TestClient
from app import app, GRID_ROWS, GRID_COLS, STEP_DELAY  # importa la aplicación y las constantes de configuración

client = TestClient(app)

def test_reset_and_get_grid():
    # Reinicia la simulación
    response_reset = client.post("/reset")
    assert response_reset.status_code == 200
    data_reset = response_reset.json()
    grid_reset = data_reset.get("grid")
    
    # Verifica que las dimensiones sean las correctas
    assert grid_reset is not None
    assert len(grid_reset) == GRID_ROWS
    assert len(grid_reset[0]) == GRID_COLS
    
    # Comprueba que el patrón inicial tenga al menos una célula viva
    count_alive = sum(sum(row) for row in grid_reset)
    assert count_alive > 0
    
    # Ahora llamamos al endpoint /grid para verificar que devuelve el mismo estado
    response_get = client.get("/grid")
    assert response_get.status_code == 200
    data_get = response_get.json()
    grid_get = data_get.get("grid")
    assert grid_get == grid_reset

def test_step_simulation():
    # Reinicia la simulación y obtiene la grilla inicial
    response_reset = client.post("/reset")
    assert response_reset.status_code == 200
    initial_grid = response_reset.json().get("grid")
    
    # Ejecuta el endpoint /step para actualizar la grilla
    response_step = client.post("/step")
    assert response_step.status_code == 200
    next_grid = response_step.json().get("grid")
    
    # Verifica que la grilla haya cambiado (en la mayoría de los casos lo hará)
    # Puede pasarse de un patrón como el glider a un estado ligeramente distinto
    # También se puede hacer una comparación de la cantidad de células vivas:
    initial_alive = sum(sum(row) for row in initial_grid)
    next_alive = sum(sum(row) for row in next_grid)
    
    # Esta verificación es básica: nos aseguramos de que la grilla no queda toda en ceros
    assert next_alive > 0
    # Y en algunos casos puede variar la cantidad total, lo cual es aceptable

def test_reset_after_steps():
    # Reinicia la simulación para obtener el estado inicial
    response_reset = client.post("/reset")
    initial_grid = response_reset.json().get("grid")
    
    # Ejecuta varios pasos
    client.post("/step")
    client.post("/step")
    
    # Reinicia la simulación nuevamente
    response_reset2 = client.post("/reset")
    new_initial_grid = response_reset2.json().get("grid")
    
    # El estado tras reiniciar debería coincidir con el estado inicial definido (ej. el glider)
    assert initial_grid == new_initial_grid

def test_custom_grid():
    """Prueba que se pueda establecer una grilla personalizada."""
    custom_grid = {
        "grid": [
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 1],
        ]
    }
    response = client.post("/grid", json=custom_grid)
    assert response.status_code == 200
    data = response.json()
    assert data["grid"] == custom_grid["grid"]

def test_reset_with_pattern():
    """Prueba que al reiniciar se utiliza el patrón especificado (por ejemplo, 'blinker')."""
    response = client.post("/reset", params={"pattern": "blinker"})
    assert response.status_code == 200
    data = response.json()
    # Verifica que la grilla tenga la dimensión esperada y que el centro tenga el patrón blinker
    assert len(data["grid"]) == GRID_ROWS
    assert len(data["grid"][0]) == GRID_COLS
    # Se puede verificar que, en el centro, hay 3 celdas en línea viva:
    mid_row = GRID_ROWS // 2
    mid_col = GRID_COLS // 2
    assert data["grid"][mid_row][mid_col - 1] == 1
    assert data["grid"][mid_row][mid_col] == 1
    assert data["grid"][mid_row][mid_col + 1] == 1

def test_step_and_back():
    """Prueba avanzar un paso y luego retroceder la simulación."""
    # Reiniciar para partir de un estado conocido
    client.post("/reset", params={"pattern": "glider"})
    response_initial = client.get("/grid")
    initial_grid = response_initial.json()["grid"]
    
    # Avanzar un paso
    response_step = client.post("/step")
    stepped_grid = response_step.json()["grid"]
    assert stepped_grid != initial_grid  # Se espera un cambio
    
    # Retroceder
    response_back = client.post("/back")
    back_grid = response_back.json()["grid"]
    assert back_grid == initial_grid

def test_start_and_pause():
    """Verifica que se pueda iniciar y pausar la simulación automática."""
    # Para probar esto de forma básica, iniciamos la simulación y esperamos un par de segundos,
    # luego la pausamos y comprobamos que el estado cambia.
    client.post("/reset", params={"pattern": "glider"})
    response_start = client.post("/start")
    started_grid = response_start.json()["grid"]
    # Esperar un poco para que se avance automáticamente
    import time
    time.sleep(STEP_DELAY * 2)
    response_pause = client.post("/pause")
    paused_grid = response_pause.json()["grid"]
    # Se espera que, al menos, el grid haya variado (pudiendo ser difícil de predecir en detalle)
    assert paused_grid != started_grid