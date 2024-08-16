import numpy as np
from tensorflow.keras.models import load_model  # type: ignore
from app.config import Config
import os

model_path = os.path.join(Config.MODEL_DIR, 'questionnaire_model.keras')

try:
    questionnaire_model = load_model(model_path)
except OSError as e:
    print(f"Error: El archivo del modelo no existe en la ruta especificada: {e}")
    questionnaire_model = None
except Exception as e:
    print(f"Error al cargar el modelo de cuestionario: {e}")
    questionnaire_model = None

def answers_preprocessing_neural_network(answers):
    try:
        if not isinstance(answers, list) or not all(isinstance(answer, str) for answer in answers):
            raise ValueError("answers debe ser una lista de strings")

        if len(answers) != 30:
            raise ValueError(f"Se esperaban 30 respuestas, pero se recibieron {len(answers)}")

        allowed_answers = {'Siempre', 'Generalmente', 'A veces', 'Rara vez', 'Nunca'}
        if not all(value in allowed_answers for value in answers):
            raise ValueError("Las respuestas contienen valores no válidos.")

        answers_array = np.array([{'Siempre': 1.0, 'Generalmente': 0.75, 'A veces': 0.50, 'Rara vez': 0.25, 'Nunca': 0.0}[value] for value in answers])
        return answers_array.reshape(1, -1)  # Asegúrate de que la forma sea (1, num_questions)
    except Exception as e:
        print(f"Error en el preprocesamiento de las respuestas: {e}")
        return None

def questionnaire_analysis_neural_network(preprocessed_answers):
    if questionnaire_model is None:
        print("El modelo de cuestionario no se cargó correctamente. No se puede realizar el análisis.")
        return None

    try:
        prediction = questionnaire_model.predict(preprocessed_answers)
        return float(prediction[0][0])
    except Exception as e:
        print(f"Error al realizar la predicción del cuestionario: {e}")
        return None