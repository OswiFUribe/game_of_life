# test_app.py
from fastapi.testclient import TestClient
from app import app, GRID_ROWS, GRID_COLS  # importa la aplicación y las constantes de configuración

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

