from app.neural_network.combined_analysis import combined_analysis

def analyze_image_and_questionnaire(image_path, qa_pairs):
    try:
        # Implementa la lógica para preprocesar la imagen
        # Analiza la imagen y las respuestas del cuestionario
        # Pasa estos datos a la red neuronal para obtener una predicción del porcentaje de autismo
        autism_score = combined_analysis(image_path=image_path, qa_pairs=qa_pairs)
        if autism_score is None:
            raise ValueError("La puntuación de autismo no se pudo calcular.")
        return autism_score
    except Exception as e:
        raise RuntimeError(f"Error en el análisis de imagen: {e}")

def analyze_video_and_questionnaire(video_path, qa_pairs):
    try:
        # Implementa la lógica para preprocesar el video
        # Analiza el video y las respuestas del cuestionario
        # Pasa estos datos a la red neuronal para obtener una predicción del porcentaje de autismo
        autism_score = combined_analysis(video_path=video_path, qa_pairs=qa_pairs)
        if autism_score is None:
            raise ValueError("La puntuación de autismo no se pudo calcular.")
        return autism_score
    except Exception as e:
        raise RuntimeError(f"Error en el análisis de video: {e}")
