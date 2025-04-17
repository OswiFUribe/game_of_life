# Juego de la Vida - Frontend

Este proyecto es la interfaz web para la simulación del "Juego de la Vida" de John Conway. Construido con Angular, el frontend se comunica con un backend desarrollado en FastAPI para controlar la simulación, mostrando el estado (la grilla) y ofreciendo controles para avanzar, retroceder, iniciar y pausar la simulación, además de permitir la definición de patrones personalizados.

## Tabla de Contenidos
- [Juego de la Vida - Frontend](#juego-de-la-vida---frontend)
  - [Tabla de Contenidos](#tabla-de-contenidos)
  - [Descripción del Proyecto](#descripción-del-proyecto)
  - [Características](#características)
  - [Arquitectura y Estructura de Archivos](#arquitectura-y-estructura-de-archivos)
  - [Instalación y Configuración](#instalación-y-configuración)
    - [Requisitos Previos](#requisitos-previos)
    - [Instalación de Dependencias](#instalación-de-dependencias)
    - [Configuración del Backend](#configuración-del-backend)
  - [Uso y Funcionalidades](#uso-y-funcionalidades)
    - [Ejecución en Desarrollo](#ejecución-en-desarrollo)
    - [Funcionalidades Clave](#funcionalidades-clave)
  - [Pruebas](#pruebas)

## Descripción del Proyecto
El frontend del "Juego de la Vida" permite a los usuarios visualizar la simulación y controlar su ejecución. Está diseñado para ofrecer una experiencia interactiva y sencilla. La comunicación se realiza a través de un servicio Angular (SimulationService) que conecta con el backend mediante peticiones HTTP.

## Características
- **Visualización Dinámica de la Grilla:**
  > Se muestra en una tabla HTML dónde cada celda representa una posición en la simulación (célula viva o muerta).

- Controles de Simulación:

- **Step:** Avanza la simulación un paso.

- **Back:** Retrocede a un estado anterior, utilizando el historial de simulación.

- **Start:** Inicia la ejecución automática (en el backend se lanza un hilo en segundo plano) y se activa el polling para actualizar la vista.

- **Pause:** Detiene la ejecución automática.

- **Reset:** Reinicia la simulación con un patrón predefinido o especificado (por ejemplo, "glider" o "blinker").

- **Definición de Grilla Personalizada:** Permite que el usuario configure manualmente un patrón específico (enviando una matriz JSON al backend).

## Arquitectura y Estructura de Archivos
La estructura básica del proyecto generado por Angular es la siguiente:

```ruby
Copiar
game-of-life-frontend/
├── e2e/                     # Pruebas end-to-end
├── node_modules/            # Dependencias NPM
├── src/
│   ├── app/
│   │   ├── grid/            # Componente que muestra la grilla y controles
│   │   │   ├── grid.component.ts
│   │   │   ├── grid.component.html
│   │   │   └── grid.component.css
│   │   ├── simulation.service.ts   # Servicio para comunicarse con el backend
│   │   ├── app.component.ts
│   │   ├── app.component.html
│   │   └── app.module.ts    (si usas NgModule) o configuración standalone en app.config.ts / main.ts
│   ├── assets/              # Imágenes, fuentes, etc.
│   ├── environments/        # Configuraciones de entorno (dev, prod)
│   └── index.html
├── angular.json             # Configuración del CLI de Angular
├── package.json             # Dependencias y scripts de NPM
├── tsconfig.json            # Configuración TypeScript
└── README.md                # Este archivo de documentación
```

> [!Note] Nota:
En proyectos con Angular 16 puedes optar por componentes standalone. En ese caso, la importación de proveedores (por ejemplo, HTTP) se hace directamente en los componentes o en un archivo de configuración (como app.config.ts) y se utiliza `bootstrapApplication` en main.ts.

## Instalación y Configuración
### Requisitos Previos
- [Node.js](https://nodejs.org/) (recomendable la última versión LTS)

- [Angular CLI](https://angular.io/cli)  
Instálalo globalmente si aún no lo tienes:

```bash
npm install -g @angular/cli
```

### Instalación de Dependencias
1. Abre una terminal en la carpeta raíz del proyecto (la misma carpeta donde se encuentra package.json).

2. Ejecuta:

```bash
npm install
```
Esto instalará todas las dependencias necesarias para el proyecto.

### Configuración del Backend

El archivo `simulation.service.ts` tiene una variable `apiUrl` que por defecto apunta a http://localhost:8000.
Asegúrate de que el backend (FastAPI) esté en ejecución y escuchando en ese puerto. Si lo ejecutas en otro puerto o dominio, actualiza la variable `apiUrl` en este archivo.

## Uso y Funcionalidades
### Ejecución en Desarrollo
Para iniciar la aplicación en modo desarrollo:

```bash
ng serve --open
```

Esto levantará el servidor de desarrollo y abrirá la aplicación en el navegador (por lo general, en http://localhost:4200).

### Funcionalidades Clave
- **GridComponent**:
  
  Muestra la grilla mediante una tabla HTML. Las celdas vivas se distinguen mediante estilos (por ejemplo, fondo negro).

- **Controles (en GridComponent):**

  - **Reset**: Reinicia la simulación con el patrón "glider" o el especificado.

  - **Step**: Avanza un paso en la simulación. Si la simulación está en ejecución automática, se pausa antes de avanzar.

  - **Back**: Retrocede al estado anterior. De igual forma, se pausa la ejecución automática si estaba activa.

  - **Start**: Inicia la ejecución automática. Se activa un mecanismo de polling para actualizar la vista cada segundo.

  - **Pause**: Detiene la actualización automática (polling).

El `SimulationService` se encarga de hacer las peticiones HTTP a los endpoints del backend para cada acción, usando métodos como GET y POST.

## Pruebas
Se han preparado pruebas unitarias para asegurar el correcto funcionamiento de los componentes y del servicio.
Para ejecutar las pruebas unitarias:

```bash
ng test
```
Esto abrirá el entorno de pruebas (usualmente Karma con Jasmine) y mostrará el resultado de cada spec.
