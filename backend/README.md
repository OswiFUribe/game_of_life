# Juego de la Vida - Backend

Este proyecto implementa el backend para "El Juego de la Vida" de John Conway con FastAPI.  
Se han implementado las siguientes funcionalidades:

- **Visualización del Estado Actual:**
  - `GET /grid`: Devuelve el estado actual de la grilla.

- **Definir una Grilla Personalizada:**
  - `POST /grid`: Permite enviar una grilla personalizada en formato JSON:
    ```json
    { "grid": [[0, 1, 0], [1, 0, 1], [0, 1, 0]] }
    ```

- **Reiniciar la Simulación:**
  - `POST /reset`: Reinicia la simulación utilizando un patrón predefinido (por defecto "glider").  
    Se puede especificar otro patrón mediante el parámetro `pattern` (por ejemplo, "blinker").

- **Avanzar la Simulación:**
  - `POST /step`: Calcula el siguiente estado de la grilla y guarda el estado anterior en un historial para permitir retroceder.

- **Retroceder la Simulación:**
  - `POST /back`: Revierte la simulación al estado anterior, usando la lista de estados guardados.

- **Ejecución Automática:**
  - `POST /start`: Inicia un modo automático en el que la simulación avanza cada cierto intervalo (configurable).
  - `POST /pause`: Pausa la ejecución automática.

## Pruebas

Se han implementado pruebas unitarias (usando pytest) tanto para la lógica de la simulación como para los endpoints de la API en los archivos `test_simulation.py` y `test_app_extended.py`.  
Para ejecutarlas:

```bash
pytest
```

## Requerimientos

Si se desea probar este proyecto por su cuenta, se recomienda crear un entorno virtual e instalar los requerimientos de `requeriments.txt`

```bash
pip install -r requirements.txt
```
