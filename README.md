# PreD TEA

## Descripción
Este proyecto implementa un sistema basado en redes neuronales artificiales para predecir y dar un diagnostico preliminar del Trastorno del Espectro Autista (TEA) en niños.

## Estructura del Proyecto

### Backend
- `app/`: Contiene la aplicación Flask y los módulos de backend.
  - `models/`: Carga el modelo de red neuronal.
  - `uploads/`: Almacenara los videos.
  - `__init__.py`: Inicializa la aplicación Flask.
  - `models`: Modelos de la base de datos.
  - `neural_network.py`: Encargada del escaneo del video.
  - `routes.py`: Define las rutas de la API.
- `cd backend`: Permite entrar en el directorio.
- `python run.py`: Script para ejecutar la aplicación Flask.