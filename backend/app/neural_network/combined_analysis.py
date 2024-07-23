from app.neural_network.image_analysis import analyze_image
from app.neural_network.video_analysis import analyze_video
from app.neural_network.questionnaire_analysis import analyze_questionnaire

def combined_analysis(image_path=None, video_path=None, qa_pairs=None):
    results = {}
    
    if image_path:
        image_result = analyze_image(image_path)
        results['image_analysis'] = image_result

    if video_path:
        video_result = analyze_video(video_path)
        results['video_analysis'] = video_result

    if qa_pairs:
        questionnaire_result = analyze_questionnaire(qa_pairs)
        results['questionnaire_analysis'] = questionnaire_result

    # Lógica para combinar los resultados de las diferentes fuentes
    combined_result = combine_results(results)
    return combined_result

def combine_results(results):
    valid_results = [value for value in results.values() if value is not None]
    
    if not valid_results:
        raise ValueError("No valid results to combine")

    combined_result = {
        'combined_autism_probability': sum(valid_results) / len(valid_results)
    }
    return combined_result
