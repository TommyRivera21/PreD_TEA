import os
import numpy as np
import h5py
from tensorflow import keras
from app.config import Config

model_path = os.path.join(Config.MODEL_DIR, 'questionnaire_model.h5')

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

# Cargar el modelo de análisis de cuestionarios
try:
    questionnaire_model = keras.models.load_model(model_path)
    print("Modelo de cuestionario cargado exitosamente")
except Exception as e:
    print(f"Error al cargar el modelo de cuestionario: {e}")
    questionnaire_model = None

def preprocess_answers(answers):
    try:
        answers_array = np.array(list(answers.values()))
        if not np.issubdtype(answers_array.dtype, np.number):
            raise ValueError("Todas las respuestas deben ser numéricas")
        return answers_array.reshape(1, -1)
    except Exception as e:
        print(f"Error en el preprocesamiento de las respuestas: {e}")
        return None

def analyze_questionnaire(answers):
    if questionnaire_model is None:
        print("El modelo de cuestionario no se cargó correctamente. No se puede realizar el análisis.")
        return None

    processed_answers = preprocess_answers(answers)
    if processed_answers is None:
        return None

    try:
        prediction = questionnaire_model.predict(processed_answers)
        return {'autism_probability': float(prediction[0][0])}
    except Exception as e:
        print(f"Error al realizar la predicción del cuestionario: {e}")
        return None

# Ejemplo de uso
if __name__ == "__main__":
    sample_answers = {
        'pregunta1': 3,
        'pregunta2': 2,
        'pregunta3': 4,
    }
    result = analyze_questionnaire(sample_answers)
    if result is not None:
        print(f"Resultado del análisis del cuestionario: {result}")
