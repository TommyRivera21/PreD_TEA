import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import Dense, Input # type: ignore
from tensorflow.keras.optimizers import Adam # type: ignore
from app.config import Config

# Mapeo de respuestas a valores numéricos con ponderación correcta
answer_mapping = {
    "Nunca": 0.0,
    "Rara vez": 0.25,
    "A veces": 0.5,
    "Generalmente": 0.75,
    "Siempre": 1.0
}

def create_questionnaire_model(num_questions):
    model = Sequential([
        Input(shape=(num_questions,)),
        Dense(64, activation='relu'),
        Dense(32, activation='relu'),
        Dense(16, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])
    return model

def load_training_data(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"El archivo de datos no existe en la ruta: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    if not isinstance(data, list) or not all(isinstance(sublist, list) for sublist in data) or not all(isinstance(entry, dict) for sublist in data for entry in sublist):
        raise ValueError("El archivo JSON debe ser una lista de listas de diccionarios")

    X = []
    y = []

    for entry in data:
        if not entry:
            continue

        num_questions = len(entry)
        answers = [answer_mapping.get(item.get("answer"), 0.0) for item in entry]
        if not all(isinstance(answer, float) for answer in answers):
            continue

        X.append(answers)
        
        # Etiqueta ficticia: Usa la media de respuestas como una etiqueta
        y.append(np.mean(answers))

    X = np.array(X)
    y = np.array(y)

    return X, y

def train_and_save_model():
    num_questions = 30
    model = create_questionnaire_model(num_questions)

    data_path = Config.QUESTIONNAIRE_TRAINING_DATA_DIR
    X, y = load_training_data(data_path)
    
    model.fit(X, y, epochs=50, batch_size=32, validation_split=0.2)
    
    model_path = os.path.join(Config.MODEL_DIR, 'questionnaire_model.keras')
    model.save(model_path)
    
    print(f"Modelo de cuestionario entrenado y guardado exitosamente en {model_path}")

if __name__ == "__main__":
    train_and_save_model()