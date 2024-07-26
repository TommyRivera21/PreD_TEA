from app.neural_network.image_analysis import analyze_image
from app.neural_network.video_analysis import analyze_video
from app.neural_network.questionnaire_analysis import analyze_questionnaire

def combined_analysis(image_path=None, video_path=None, qa_pairs=None):
    results = []
    
    if image_path:
        try:
            image_result = analyze_image(image_path)
            results.append(image_result)
        except Exception as e:
            print(f"Error analyzing image: {e}")

    if video_path:
        try:
            video_result = analyze_video(video_path)
            results.append(video_result)
        except Exception as e:
            print(f"Error analyzing video: {e}")

    if qa_pairs:
        try:
            questionnaire_result = analyze_questionnaire(qa_pairs)
            results.append(questionnaire_result)
        except Exception as e:
            print(f"Error analyzing questionnaire: {e}")

    if not results:
        raise ValueError("No valid results to combine")

    return combine_results(results)

def combine_results(results):
    if not results:
        raise ValueError("No valid results to combine")

    combined_result = sum(results) / len(results)
    return combined_result
