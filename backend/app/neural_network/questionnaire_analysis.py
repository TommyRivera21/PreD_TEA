import numpy as np
from tensorflow.keras.models import load_model  # type: ignore
from app.config import Config
import os

model_path = os.path.join(Config.MODEL_DIR, 'questionnaire_model.h5')
questionnaire_model = load_model(model_path)

def answers_preprocessing_neural_network(answers):
    try:
        # Verificar que `answers` sea una lista de strings
        if not isinstance(answers, list) or not all(isinstance(answer, str) for answer in answers):
            raise ValueError("answers debe ser una lista de strings")

        if len(answers) != 30:
            raise ValueError(f"Se esperaban 30 respuestas, pero se recibieron {len(answers)}")

        # Crear un array de respuestas preprocesadas
        answers_array = []
        for value in answers:
            if value not in ['Siempre', 'Generalmente', 'A veces', 'Rara vez', 'Nunca']:
                raise ValueError(f"Respuesta no válida: {value}")
            answers_array.append({'Siempre': 1.0, 'Generalmente': 0.75, 'A veces': 0.50, 'Rara vez': 0.25, 'Nunca': 0.0}[value])

        return np.array(answers_array)
    except Exception as e:
        print(f"Error en el preprocesamiento de las respuestas: {e}")
        return None

def questionnaire_analysis_neural_network(preprocessed_answers):
    if questionnaire_model is None:
        print("El modelo de cuestionario no se cargó correctamente. No se puede realizar el análisis.")
        return None

    try:
        # Asegurarse de que la entrada tenga la forma correcta
        preprocessed_answers = preprocessed_answers.reshape(1, -1)
        prediction = questionnaire_model.predict(preprocessed_answers)
        return float(prediction[0][0])
    except Exception as e:
        print(f"Error al realizar la predicción del cuestionario: {e}")
        return None