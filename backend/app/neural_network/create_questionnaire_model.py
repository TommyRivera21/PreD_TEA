import sys
import os
import tensorflow as tf
from tensorflow.keras.models import Sequential  # type: ignore
from tensorflow.keras.layers import Dense  # type: ignore
from app.config import Config

# Añadir el directorio raíz al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

def create_questionnaire_model(num_questions):
    model = Sequential([
        Dense(64, activation='relu', input_shape=(num_questions,)),  # Número de unidades, función de activación
        Dense(32, activation='relu'),
        Dense(16, activation='relu'),
        Dense(1, activation='sigmoid')  # Número de unidades en la capa de salida, función de activación
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])  # Optimizador, función de pérdida, métricas
    return model

# Define the number of questions in the questionnaire
num_questions = 30  # Asegúrate de que este número coincide con el número de preguntas en tu cuestionario

if __name__ == "__main__":
    questionnaire_model = create_questionnaire_model(num_questions)
    
    # Crear el directorio si no existe
    os.makedirs(Config.MODEL_DIR, exist_ok=True)
    
    # Guardar el modelo en la ruta especificada
    model_path = os.path.join(Config.MODEL_DIR, 'questionnaire_model.h5')
    questionnaire_model.save(model_path)
    
    print(f"Modelo de cuestionario guardado exitosamente en {model_path}")
