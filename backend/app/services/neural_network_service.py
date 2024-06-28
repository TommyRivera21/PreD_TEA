from app.neural_network.combined_analysis import combined_analysis

def analyze_image_and_questionnaire(image_path, questionnaire_answers):
    # Implementa la lógica exacta para preprocesar la imagen, analizar la imagen y las respuestas del cuestionario,
    # y luego pasar estos datos a la red neuronal para obtener una predicción del porcentaje de autismo.
    autism_score = combined_analysis(image_path=image_path, questionnaire_answers=questionnaire_answers)
    return autism_score

def analyze_video_and_questionnaire(video_path, questionnaire_answers):
    # Implementa la lógica exacta para preprocesar el video, analizar el video y las respuestas del cuestionario,
    # y luego pasar estos datos a la red neuronal para obtener una predicción del porcentaje de autismo.
    autism_score = combined_analysis(video_path=video_path, questionnaire_answers=questionnaire_answers)
    return autism_score
