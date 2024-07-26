import os
import cv2
import numpy as np
from tensorflow import keras
from app.config import Config

# Ruta del modelo
model_path = os.path.join(Config.MODEL_DIR, 'image_model.h5')

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

# Cargar el modelo de análisis de imágenes
try:
    image_model = keras.models.load_model(model_path)
    print("Modelo cargado exitosamente")
except Exception as e:
    raise RuntimeError(f"Error al cargar el modelo: {e}")

def preprocess_image(image_path):
    try:
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"No se pudo cargar la imagen: {image_path}")
        image = cv2.resize(image, (128, 128))  # Ajusta el tamaño de la imagen aquí
        image = image / 255.0
        processed_image = np.expand_dims(image, axis=0)
        print(f"Forma de la imagen procesada: {processed_image.shape}")  # Registro para verificar la forma
        return processed_image
    except Exception as e:
        raise RuntimeError(f"Error en el preprocesamiento de la imagen: {e}")
    
def analyze_image(image_path):
    if image_model is None:
        raise RuntimeError("El modelo no se cargó correctamente. No se puede realizar el análisis.")

    processed_image = preprocess_image(image_path)
    if processed_image is None:
        raise RuntimeError("Error en el preprocesamiento de la imagen.")

    try:
        prediction = image_model.predict(processed_image)
        print(f"Predicción cruda: {prediction}")  # Registro para verificar la salida
        return prediction[0][0]
    except Exception as e:
        raise RuntimeError(f"Error al realizar la predicción: {e}")
    
# Ejemplo de uso
if __name__ == "__main__":
    test_image_path = os.path.join('uploads', 'images', 'test_image.jpg')  # Ajusta la ruta del test_image aquí
    try:
        result = analyze_image(test_image_path)
        if result is not None:
            print(f"Resultado del análisis: {result}")
    except Exception as e:
        print(f"Error en el análisis: {e}")
