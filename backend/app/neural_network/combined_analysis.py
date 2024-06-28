from .image_analysis import analyze_image
from .video_analysis import analyze_video
from .questionnaire_analysis import analyze_questionnaire

def combined_analysis(image_path=None, video_path=None, questionnaire_answers=None):
    image_score = 0
    video_score = 0
    questionnaire_score = 0

    if image_path:
        image_score = analyze_image(image_path)
    if video_path:
        video_score = analyze_video(video_path)
    if questionnaire_answers:
        questionnaire_score = analyze_questionnaire(questionnaire_answers)

    # Combina los puntajes de alguna manera para obtener el puntaje final
    # Esta es una implementación simple, puedes ajustar el peso de cada componente
    final_score = (image_score + video_score + questionnaire_score) / 3
    return final_score
