import os
from flask_jwt_extended import jwt_required
from flask import Blueprint, request, jsonify
from app.neural_network.image_analysis import analyze_image
from app.neural_network.video_analysis import analyze_video
from app.neural_network.questionnaire_analysis import analyze_questionnaire
from app.neural_network.combined_analysis import combined_analysis
from app.config import Config


results_bp = Blueprint('results', __name__, url_prefix='/results')

@results_bp.route('/analyze_image', methods=['POST'])
def analyze_image_endpoint():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image = request.files['image']
    image_path = os.path.join(Config.UPLOADED_PHOTOS_DEST, image.filename)
    image.save(image_path)

    try:
        result = analyze_image(image_path)
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@results_bp.route('/analyze_video', methods=['POST'])
def analyze_video_endpoint():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    video = request.files['video']
    video_path = os.path.join(Config.UPLOADED_VIDEOS_DEST, video.filename)
    video.save(video_path)

    try:
        result = analyze_video(video_path)
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@results_bp.route('/analyze_questionnaire', methods=['POST'])
def analyze_questionnaire_endpoint():
    data = request.get_json()
    questionnaire_answers = data.get('questionnaire_answers', {})

    try:
        result = analyze_questionnaire(questionnaire_answers)
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@results_bp.route('/analyze_combined', methods=['POST'])
def analyze_combined_endpoint():
    data = request.form.to_dict()
    questionnaire_answers = data.get('questionnaire_answers', {})

    image_path = None
    video_path = None

    if 'image' in request.files:
        image = request.files['image']
        image_path = os.path.join(Config.UPLOADED_PHOTOS_DEST, image.filename)
        image.save(image_path)

    if 'video' in request.files:
        video = request.files['video']
        video_path = os.path.join(Config.UPLOADED_VIDEOS_DEST, video.filename)
        video.save(video_path)

    try:
        result = combined_analysis(image_path=image_path, video_path=video_path, questionnaire_answers=questionnaire_answers)
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500