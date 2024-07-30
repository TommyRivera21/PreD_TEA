import os
import cv2
import numpy as np
from tensorflow import keras
from app.config import Config

# Ruta del modelo
model_path = os.path.join(Config.MODEL_DIR, 'video_model.h5')

# Verificar existencia y tamaño del archivo
if os.path.exists(model_path):
    print(f"El archivo existe y su tamaño es: {os.path.getsize(model_path)} bytes")
else:
    print(f"El archivo no existe en la ruta: {model_path}")

# Intentar abrir el archivo manualmente
try:
    with open(model_path, 'rb') as f:
        print("Archivo abierto correctamente")
except Exception as e:
    print(f"Error al abrir el archivo: {e}")

# Cargar el modelo de análisis de videos
try:
    video_model = keras.models.load_model(model_path)
    print("Modelo cargado exitosamente")
except Exception as e:
    raise RuntimeError(f"Error al cargar el modelo: {e}")

def video_preprocessing_neural_network(video_path):
    try:
        cap = cv2.VideoCapture(video_path)
        frames = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (64, 64))  # Ajusta el tamaño de los frames aquí
            frame = frame / 255.0
            frames.append(frame)
        cap.release()
        frames = np.array(frames)
        
        # Aplanar cada frame de (64, 64, 3) a (12288)
        frames = frames.reshape(frames.shape[0], 64*64*3)
        
        # Agregar una dimensión adicional para el batch
        frames = np.expand_dims(frames, axis=0)
        
        print(f"Forma de los frames procesados: {frames.shape}")  # Registro para verificar la forma
        return frames
    except Exception as e:
        raise RuntimeError(f"Error en el preprocesamiento del video: {e}")

def video_analysis_neural_network(video_path):
    if video_model is None:
        raise RuntimeError("El modelo no se cargó correctamente. No se puede realizar el análisis.")

    processed_video = video_preprocessing_neural_network(video_path)
    if processed_video is None:
        raise RuntimeError("Error en el preprocesamiento del video.")

    try:
        prediction = video_model.predict(processed_video)
        print(f"Predicción cruda: {prediction}")  # Registro para verificar la salida
        return prediction[0][0]
    except Exception as e:
        raise RuntimeError(f"Error al realizar la predicción: {e}")