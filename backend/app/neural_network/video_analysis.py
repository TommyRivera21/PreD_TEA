import os
import cv2
import numpy as np
from tensorflow import keras
from app.config import Config

# Ruta del modelo
model_path = os.path.join(Config.MODEL_DIR, 'video_model.keras')

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
    video_model.summary()  # Imprime el resumen del modelo para verificar la arquitectura
except Exception as e:
    raise RuntimeError(f"Error al cargar el modelo: {e}")

def video_preprocessing_neural_network(video_path, num_frames=10, img_height=64, img_width=64):
    try:
        cap = cv2.VideoCapture(video_path)
        frames = []
        while len(frames) < num_frames:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (img_width, img_height))  # Ajusta el tamaño de los frames aquí
            frame = frame / 255.0
            frames.append(frame)
        cap.release()

        # Si hay menos frames que num_frames, rellena con el último frame
        while len(frames) < num_frames:
            frames.append(frames[-1])
        
        frames = np.array(frames)
        # Asegúrate de que la forma sea [1, num_frames, img_height, img_width, num_channels]
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
        return prediction[0][0]  # Ajustar si es necesario
    except Exception as e:
        raise RuntimeError(f"Error al realizar la predicción: {e}")