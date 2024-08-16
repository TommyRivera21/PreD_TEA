import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    UPLOADED_PHOTOS_DEST = os.getenv('UPLOADED_PHOTOS_DEST')
    UPLOADED_VIDEOS_DEST = os.getenv('UPLOADED_VIDEOS_DEST')
    MODEL_DIR = os.getenv('MODEL_PATH')
    TRAINING_DATA_DIR = os.getenv('TRAINING_DATA_PATH')
    VALIDATION_DATA_DIR = os.getenv('VALIDATION_DATA_PATH')
    GENERATION_QUESTIONNAIRE_TRAINING_DATA_DIR = os.getenv('GENERATION_QUESTIONNAIRE_TRAINING_DATA_PATH')
    QUESTIONNAIRE_TRAINING_DATA_DIR = os.getenv('QUESTIONNAIRE_TRAINING_DATA_PATH')
    
# Verificar las rutas de destino
print(f"Ruta para fotos: {Config.UPLOADED_PHOTOS_DEST}")
print(f"Ruta para videos: {Config.UPLOADED_VIDEOS_DEST}")
print(f"Ruta para modelos: {Config.MODEL_DIR}")
print(f"Ruta para datos de entrenamiento: {Config.TRAINING_DATA_DIR}")
print(f"Ruta para datos de validación: {Config.VALIDATION_DATA_DIR}")
print(f"Ruta para datos de cuestionario generados: {Config.GENERATION_QUESTIONNAIRE_TRAINING_DATA_DIR}")
print(f"Ruta para datos de cuestionario: {Config.QUESTIONNAIRE_TRAINING_DATA_DIR}")
