# El Juego de la Vida - Simulación Web Interactiva

Este proyecto es una implementación web del clásico autómata celular "[The Game of Life](https://conwaylife.com/)" de John Conway. La aplicación se compone de dos partes principales:

- Backend en Python:
    
    Encargado de la lógica de simulación, el backend calculará la evolución de la grilla siguiendo las reglas del juego. además, expondrá una API REST (y posiblemente un canal de WebSockets para actualizaciones en tiempo real) que permitirá interactuar con el estado de la simulación.

- Frontend en Angular

    Este componente se encargará de la visualización de la grilla y de proporcionar una interfaz interactiva para iniciar, pausar, reiniciar y ajustar parámetros de la simulación. La idea es que la página web sea sencilla pero eficaz, facilitando la interacción del usuario.

La estructura de documentos de este proyecto es la siguiente:

- 