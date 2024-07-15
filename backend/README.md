# PreD TEA

## Descripción
Este proyecto implementa un sistema basado en redes neuronales artificiales para predecir y dar un diagnostico preliminar del Trastorno del Espectro Autista (TEA) en niños.

#### Ejectur el proyecto
- `cd backend`: Permite entrar en el directorio.
- `python manage.py`: Script para ejecutar la aplicación Flask.

## Estructura del Proyecto

### Backend
- `app/`: Contiene la aplicación Flask y los módulos de backend.
  - `__init__.py`: Inicializa la aplicación Flask.
  - `config.py`: Configuracion para la variables de entorno.
  - `models`: Modelos de la base de datos.
  - `neural_network.py`: Procesa el video, imagenes, questionario y reliza la prediccion.
- `uploads/`: Almacenara los videos e imagenes
- `models/`: Carga los modelos de red neuronal.
- `neural_network/`: Contiene la logica para procesar las imagenes, videos y questionarios.
- `routes/`: Contiene las rutas de la API.
- `services/`: Contiene los servicios para las rutas.