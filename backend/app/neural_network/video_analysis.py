import os
import cv2
import numpy as np
import h5py
from tensorflow import keras
from app.config import Config

# Actualiza la ruta del modelo para que apunte al directorio correcto
model_path = os.path.join(Config.MODEL_DIR, 'video_model.h5')

# Verificar la existencia y el tamaño del archivo
if os.path.exists(model_path):
    print(f"El archivo existe y su tamaño es: {os.path.getsize(model_path)} bytes")
else:
    print(f"El archivo no existe en la ruta: {model_path}")

# Intentar abrir el archivo manualmente
try:
    with h5py.File(model_path, 'r') as f:
        print("Archivo abierto correctamente")
        print("Claves en el archivo:", list(f.keys()))
except Exception as e:
    print(f"Error al abrir el archivo: {e}")

# Cargar el modelo de análisis de videos
try:
    video_model = keras.models.load_model(model_path)
    print("Modelo de video cargado exitosamente")
except Exception as e:
    print(f"Error al cargar el modelo de video: {e}")
    video_model = None

def preprocess_video(video_path):
    try:
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"No se pudo abrir el video: {video_path}")
        
        frames = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (64, 64))  # Ajusta el tamaño de los frames aquí
            frame = frame / 255.0
            frames.append(frame)
        cap.release()
        
        if len(frames) == 0:
            raise ValueError("No se pudieron extraer frames del video")
        
        return np.array(frames)
    except Exception as e:
        print(f"Error en el preprocesamiento del video: {e}")
        return None

def analyze_video(video_path):
    if video_model is None:
        print("El modelo de video no se cargó correctamente. No se puede realizar el análisis.")
        return None

    processed_video = preprocess_video(video_path)
    if processed_video is None:
        return None

    try:
        processed_video = np.expand_dims(processed_video, axis=0)
        prediction = video_model.predict(processed_video)
        return prediction[0][0]
    except Exception as e:
        print(f"Error al realizar la predicción del video: {e}")
        return None

# Ejemplo de uso
if __name__ == "__main__":
    test_video_path = os.path.join('uploads', 'videos', 'test_video.mp4')  # Ajusta la ruta del test_video aquí
    result = analyze_video(test_video_path)
    if result is not None:
        print(f"Resultado del análisis del video: {result}")
