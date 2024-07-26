import logging
import numpy as np
from app.neural_network.combined_analysis import combined_analysis

# Configura el logger
logger = logging.getLogger(__name__)

def analyze_image_and_questionnaire(image_path, qa_pairs):
    try:
        # Llama a combined_analysis y obtiene la puntuación de autismo
        autism_score = combined_analysis(image_path=image_path, qa_pairs=qa_pairs)
        
        # Registra el tipo y valor de autism_score para depuración
        logger.debug(f"Puntuación de autismo recibida: {autism_score}, Tipo: {type(autism_score)}")
        
        # Maneja el caso en que autism_score sea un arreglo numpy
        if isinstance(autism_score, np.ndarray):
            if autism_score.size == 1:
                autism_score = float(autism_score[0])
            else:
                raise ValueError("La puntuación de autismo es un arreglo numpy con más de un elemento.")
        
        # Verifica si autism_score es un número
        if autism_score is None:
            raise ValueError("La puntuación de autismo es None.")
        if not isinstance(autism_score, (int, float)):
            raise ValueError("La puntuación de autismo no es un número.")
        if not (0 <= autism_score <= 100):
            raise ValueError("La puntuación de autismo está fuera del rango esperado (0 a 100).")
        
        return autism_score
    
    except Exception as e:
        # Registra el error con un mensaje más descriptivo
        logger.error(f"Error al analizar la imagen y el cuestionario: {e}")
        raise RuntimeError(f"Error en el análisis de imagen y cuestionario: {e}")

def analyze_video_and_questionnaire(video_path, qa_pairs):
    try:
        autism_score = combined_analysis(video_path=video_path, qa_pairs=qa_pairs)
        
        # Maneja el caso en que autism_score sea un arreglo numpy
        if isinstance(autism_score, np.ndarray):
            if autism_score.size == 1:
                autism_score = float(autism_score[0])
            else:
                raise ValueError("La puntuación de autismo es un arreglo numpy con más de un elemento.")
        
        if autism_score is None or not (0 <= autism_score <= 100):
            raise ValueError("La puntuación de autismo es inválida o no se pudo calcular correctamente.")
        
        return autism_score
    except Exception as e:
        logger.error(f"Error analyzing video: {e}")
        raise RuntimeError(f"Error en el análisis de video: {e}")