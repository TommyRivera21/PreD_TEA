import logging
import numpy as np
import json
from app.models import Questionnaire, db, Image, Video
from app.neural_network.image_analysis import image_analysis_neural_network
from app.neural_network.video_analysis import video_analysis_neural_network
from app.neural_network.questionnaire_analysis import questionnaire_analysis_neural_network, answers_preprocessing_neural_network

# Configura el logger
logger = logging.getLogger(__name__)

def image_analysis_service(image_id, image_path):
    try:
        # Ejecutar análisis de imagen
        autism_score = image_analysis_neural_network(image_path)
        logger.info(f"Análisis de imagen: {image_path} - Score: {autism_score}")
        
        # Convertir float32 a float si es necesario
        autism_score = float(autism_score) if isinstance(autism_score, np.float32) else autism_score
        
        # Guardar el resultado en la base de datos
        image = Image.query.get(image_id)
        if image:
            image.image_prediction_score = autism_score
            db.session.commit()
            logger.info(f"Imagen {image_id} actualizada con el score: {autism_score}")
        else:
            logger.error(f"No se encontró la imagen con ID: {image_id}")
        
        return {"prediction_score": autism_score}
    except Exception as e:
        logger.error(f"Error analyzing image {image_id}: {e}")
        raise RuntimeError(f"Error analyzing image {image_id}: {e}")

def calculate_average_score(diagnostic_id):
    try:
        images = Image.query.filter_by(diagnostic_id=diagnostic_id).all()
        if not images:
            logger.warning(f"No se encontraron imágenes para el diagnóstico ID {diagnostic_id}")
            return 0.0

        scores = [image.image_prediction_score for image in images if image.image_prediction_score is not None]
        if not scores:
            logger.warning(f"No se encontraron puntuaciones válidas para el diagnóstico ID {diagnostic_id}")
            return 0.0

        average_score = np.mean(scores)
        
        logger.info(f"Promedio de las predicciones para el diagnóstico ID {diagnostic_id}: {average_score:.2f}")
        return average_score
    except Exception as e:
        logger.error(f"Error calculating average score for diagnostic ID {diagnostic_id}: {e}")
        raise RuntimeError(f"Error calculating average score for diagnostic ID {diagnostic_id}: {e}")

def video_analysis_service(video_id, video_path):
    try:
        autism_score = video_analysis_neural_network(video_path)
        logger.info(f"Análisis de video: {video_path} - Score: {autism_score}")
        
        # Convertir float32 a float si es necesario
        autism_score = float(autism_score) if isinstance(autism_score, np.float32) else autism_score
        
        # Guardar el resultado en la base de datos
        video = Video.query.get(video_id)
        if video:
            video.video_prediction_score = autism_score
            db.session.commit()
            logger.info(f"Video {video_id} actualizado con el score: {autism_score}")
        else:
            logger.error(f"No se encontró el video con ID: {video_id}")
        
        return {"prediction_score": autism_score}
    except Exception as e:
        logger.error(f"Error analyzing video: {e}")
        raise RuntimeError(f"Error analyzing video: {e}")

def questionnaire_analysis_service(questionnaire_id, qa_pairs):
    try:
        # Convertir la cadena JSON a una lista de diccionarios si es necesario
        if isinstance(qa_pairs, str):
            qa_pairs = json.loads(qa_pairs)
        
        # Extraer solo las respuestas de qa_pairs
        answers = [pair['answer'] for pair in qa_pairs]
        
        # Preprocesar las respuestas del cuestionario
        preprocessed_answers = answers_preprocessing_neural_network(answers)
        if preprocessed_answers is None:
            raise ValueError("Error en el preprocesamiento de las respuestas")

        # Realizar la predicción utilizando el modelo de red neuronal
        autism_probability = questionnaire_analysis_neural_network(preprocessed_answers)
        if autism_probability is None:
            raise ValueError("Resultado de predicción no válido de la red neuronal")
        
        print(f"Predicción del cuestionario: {autism_probability}")  # Imprimir el valor de la predicción
        
        # Guardar el resultado en la base de datos
        questionnaire = Questionnaire.query.get(questionnaire_id)
        if questionnaire:
            questionnaire.questionnaire_prediction_score = autism_probability
            db.session.commit()
            logger.info(f"Cuestionario {questionnaire_id} actualizado con el valor de prediccion: {autism_probability}")
        else:
            logger.error(f"No se encontró el cuestionario con ID: {questionnaire_id}")
        
        return {"prediction_score": autism_probability}
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Error al decodificar JSON: {e}")
    except Exception as e:
        raise RuntimeError(f"Error analyzing questionnaire: {e}")