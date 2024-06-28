import cv2
import numpy as np
import os
import h5py
from tensorflow import keras

# Obtener la ruta absoluta del directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))
# Ir dos directorios hacia arriba para llegar a la raíz del proyecto
base_dir = os.path.dirname(os.path.dirname(current_dir))
model_path = os.path.join(base_dir, 'models', 'image_model.h5')

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

# Cargar el modelo de análisis de imágenes
try:
    image_model = keras.models.load_model(model_path)
    print("Modelo cargado exitosamente")
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    # Aquí puedes agregar lógica adicional, como cargar un modelo de respaldo
    image_model = None

def preprocess_image(image_path):
    try:
        # Implementa la lógica de preprocesamiento de imágenes
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"No se pudo cargar la imagen: {image_path}")
        image = cv2.resize(image, (224, 224))  # Asumiendo que el modelo espera una entrada de 224x224
        image = image / 255.0  # Normalizar los valores de los píxeles
        return np.expand_dims(image, axis=0)
    except Exception as e:
        print(f"Error en el preprocesamiento de la imagen: {e}")
        return None

def analyze_image(image_path):
    if image_model is None:
        print("El modelo no se cargó correctamente. No se puede realizar el análisis.")
        return None

    processed_image = preprocess_image(image_path)
    if processed_image is None:
        return None

    try:
        prediction = image_model.predict(processed_image)
        return prediction[0][0]  # Asumiendo que el modelo devuelve una predicción de un solo valor
    except Exception as e:
        print(f"Error al realizar la predicción: {e}")
        return None

# Ejemplo de uso
if __name__ == "__main__":
    test_image_path = os.path.join(base_dir, 'path', 'to', 'test_image.jpg')
    result = analyze_image(test_image_path)
    if result is not None:
        print(f"Resultado del análisis: {result}")