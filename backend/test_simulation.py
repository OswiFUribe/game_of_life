import pytest
from simulation import get_next_state

def test_block_stable():
    """
    Prueba con el patrón "block" (cuadrado estable) que no debe cambiar.
    """
    grid = [
        [0, 0, 0, 0],
        [0, 1, 1, 0],
        [0, 1, 1, 0],
        [0, 0, 0, 0],
    ]
    # El patrón estable no debe variar en la siguiente iteración
    next_grid = get_next_state(grid)
    assert next_grid == grid

def test_blinker_oscillator():
    """
    Prueba con el patrón "blinker" (oscilador de 3 celdas) que cambia de orientación.
    """
    # Estado inicial: línea horizontal
    grid = [
        [0, 0, 0],
        [1, 1, 1],
        [0, 0, 0],
    ]
    # Estado esperado: línea vertical
    expected_grid = [
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
    ]
    next_grid = get_next_state(grid)
    assert next_grid == expected_grid

def test_empty_grid():
    """
    Verifica que una grilla completamente vacía se mantiene vacía.
    """
    grid = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]
    next_grid = get_next_state(grid)
    assert next_grid == grid
    
def test_single_cell_dies():
    """
    Verifica que una célula aislada muere por falta de vecinos.
    """
    grid = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0],
    ]
    expected_grid = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]
    next_grid = get_next_state(grid)
    assert next_grid == expected_grid

def test_two_adjacent_cells_die():
    """
    Verifica que dos células adyacentes mueren por no tener suficientes vecinos.
    """
    grid = [
        [0, 0, 0],
        [0, 1, 1],
        [0, 0, 0],
    ]
    expected_grid = [
        [0, 0, 0],
        [0, 0, 0],
        [0, 0, 0],
    ]
    next_grid = get_next_state(grid)
    assert next_grid == expected_grid

def test_minimal_grid():
    """
    Verifica la simulación en una grilla mínima (1x1).
    """
    grid = [[1]]
    # Una única célula sin vecinos siempre muere.
    expected_grid = [[0]]
    next_grid = get_next_state(grid)
    assert next_grid == expected_grid

def test_no_mutation():
    """
    Verifica que la grilla original no se modifica al calcular el siguiente estado.
    """
    grid = [
        [0, 1, 0],
        [1, 0, 1],
        [0, 1, 0],
    ]
    grid_copy = [row[:] for row in grid]  # Crea una copia profunda.
    _ = get_next_state(grid)
    assert grid == grid_copy

