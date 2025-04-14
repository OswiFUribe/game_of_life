import time
import os

def get_next_state(grid):
    """
    Calcula el siguiente estado del tablero basado en las reglas del Juego de la Vida.

    Args:
        grid (list[list[int]]): Estado actual del tablero (lista de listas) donde 1 representa una célula viva y 0 una célula muerta.

    Returns:
        list[list[int]]: Nuevo estado del tablero.
    """
    rows = len(grid)
    cols = len(grid[0])
    new_grid = [[0 for _ in range(cols)] for _ in range(rows)]
    
    for i in range(rows):
        for j in range(cols):
            live_neighbors = 0
            # Itera sobre las celdas vecinas (incluye bordes)
            for x in range(max(0, i - 1), min(rows, i + 2)):
                for y in range(max(0, j - 1), min(cols, j + 2)):
                    if (x, y) != (i, j):
                        live_neighbors += grid[x][y]
            
            # Aplica las reglas:
            if grid[i][j] == 1:
                # Regla 1 y 3: Supervivencia
                if live_neighbors in (2, 3):
                    new_grid[i][j] = 1
                else:
                    new_grid[i][j] = 0
            else:
                # Regla 4: Reproducción
                if live_neighbors == 3:
                    new_grid[i][j] = 1
                else:
                    new_grid[i][j] = 0
    
    return new_grid

def print_grid(grid):
    """
    Imprime el estado del tablero en la consola. Se usa '■' para representar una célula viva y un espacio en blanco para una muerta.
    Además, se limpia la pantalla en cada iteración para ver la evolución en tiempo real.
    """
    # Limpia la pantalla (compatible con Windows y Unix)
    os.system('cls' if os.name == 'nt' else 'clear')
    for row in grid:
        line = ''.join(['■' if cell else ' ' for cell in row])
        print(line)

def create_initial_grid(rows, cols):
    """
    Crea un tablero vacío de tamaño rows x cols e inserta una configuración inicial (por ejemplo, un "glider").

    Args:
        rows (int): Número de filas.
        cols (int): Número de columnas.

    Returns:
        list[list[int]]: Tablero inicial.
    """
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    
    # Configuración de glider (puedes cambiar las coordenadas para otras formaciones)
    glider = [(1, 2), (2, 3), (3, 1), (3, 2), (3, 3)]
    for i, j in glider:
        if i < rows and j < cols:  # Asegurarse que las coordenadas estén dentro del tablero
            grid[i][j] = 1
    return grid

def main():
    # Define el tamaño del tablero
    rows, cols = 20, 40
    grid = create_initial_grid(rows, cols)

    try:
        while True:
            print_grid(grid)
            grid = get_next_state(grid)
            time.sleep(0.5)  # Espera 0.5 segundos para observar la evolución
    except KeyboardInterrupt:
        print("Simulación terminada.")

if __name__ == '__main__':
    main()
