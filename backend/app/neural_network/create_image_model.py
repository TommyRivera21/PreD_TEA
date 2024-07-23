import sys
import os
from tensorflow.keras.models import Sequential  # type: ignore
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense  # type: ignore

# Añadir el directorio raíz al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.config import Config

def create_image_model():
    model = Sequential([
        Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
    return model

if __name__ == "__main__":
    image_model = create_image_model()
    
    # Crear el directorio si no existe
    os.makedirs(Config.MODEL_DIR, exist_ok=True)
    
    # Guardar el modelo en la ruta especificada
    model_path = os.path.join(Config.MODEL_DIR, 'image_model.h5')
    image_model.save(model_path)
    
    print(f"Modelo de imagen guardado exitosamente en {model_path}")
