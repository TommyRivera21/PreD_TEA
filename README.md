# PreD TEA

## Descripción
Este proyecto implementa un sistema basado en redes neuronales artificiales para predecir y dar un diagnostico preliminar del Trastorno del Espectro Autista (TEA) en niños.

#### Ejecucion del proyecto
- `cd backend`: Permite entrar en el directorio.
- `python manage.py run`: Script para ejecutar la aplicación Flask.

## Estructura del Proyecto

### Backend
- `app/`: Contiene la aplicación Flask y los módulos de backend.
  - `__init__.py`: Inicializa la aplicación Flask.
  - `config.py`: Configuracion para la variables de entorno.
  - `models.py`: Modelos de la base de datos.
  - `data/`: Contiene los datos el entranamiento de los modelos imagen, video y questionnaire.
  - `neural_network/`: Contiene la logica para procesar las imagenes, videos y cuestionarios.
    - `models/`: Carga los modelos de red neuronal.
  - `routes/`: Contiene las rutas de la API.
  - `services/`: Contiene los servicios para las rutas.
- `uploads/`: Almacenara los videos e imagenes