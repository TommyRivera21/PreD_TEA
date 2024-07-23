import sys
import os
import tensorflow as tf
from tensorflow.keras.models import Sequential  # type: ignore
from tensorflow.keras.layers import Dense, LSTM  # type: ignore

# Añadir el directorio raíz al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.config import Config

def create_video_model():
    model = Sequential([
        # La capa LSTM espera una entrada de 3D [batch_size, timesteps, features]
        LSTM(64, return_sequences=True, input_shape=(None, 64*64*3)),  # Adaptar según el tamaño del frame
        LSTM(32),
        Dense(16, activation='relu'),
        Dense(1, activation='sigmoid')  # Número de unidades en la capa de salida, función de activación
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])  # Optimizador, función de pérdida, métricas
    return model

if __name__ == "__main__":
    video_model = create_video_model()
    
    # Crear el directorio si no existe
    os.makedirs(Config.MODEL_DIR, exist_ok=True)
    
    # Guardar el modelo en la ruta especificada
    model_path = os.path.join(Config.MODEL_DIR, 'video_model.h5')
    video_model.save(model_path)
    
    print(f"Modelo de video guardado exitosamente en {model_path}")
