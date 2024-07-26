import os
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import Blueprint, request, jsonify
from app.neural_network.image_analysis import analyze_image
from app.neural_network.video_analysis import analyze_video
from app.neural_network.questionnaire_analysis import analyze_questionnaire
from app.neural_network.combined_analysis import combined_analysis
from app.config import Config
from app.models import Result
from app.services.diagnosticService import DiagnosticService
from app.services.resultService import ResultService

results_bp = Blueprint('results', __name__, url_prefix='/results')

@results_bp.route('/<int:diagnostic_id>', methods=['GET'])
@jwt_required()
def get_results(diagnostic_id):
    try:
        user_id = get_jwt_identity()
        diagnostic = DiagnosticService.get_diagnostic(diagnostic_id)
        
        if not diagnostic or diagnostic.user_id != user_id:
            return jsonify({"error": "Diagnostic not found or unauthorized"}), 404

        result = Result.query.filter_by(diagnostic_id=diagnostic_id).first()
        
        if not result:
            return jsonify({"error": "Results not available yet"}), 404

        return jsonify({
            "combined_autism_probability": result.autism_score
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@results_bp.route('/analyze_image', methods=['POST'])
@jwt_required()
def analyze_image_endpoint():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    image = request.files['image']
    image_path = os.path.join(Config.UPLOADED_PHOTOS_DEST, image.filename)
    image.save(image_path)
    
    user_id = get_jwt_identity()

    try:
        autism_score = analyze_image(image_path)
        
        # Crear o actualizar el resultado en la base de datos
        diagnostic_id = DiagnosticService.create_diagnostic(user_id)  # O define cómo obtener el diagnostic_id
        result = ResultService.create_or_update_result(user_id, diagnostic_id, autism_score)
        
        return jsonify({'result_id': result.id, 'autism_score': autism_score}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@results_bp.route('/analyze_video', methods=['POST'])
@jwt_required()
def analyze_video_endpoint():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400

    video = request.files['video']
    video_path = os.path.join(Config.UPLOADED_VIDEOS_DEST, video.filename)
    video.save(video_path)
    
    user_id = get_jwt_identity()

    try:
        autism_score = analyze_video(video_path)
        
        # Crear o actualizar el resultado en la base de datos
        diagnostic_id = DiagnosticService.create_diagnostic(user_id)  # O define cómo obtener el diagnostic_id
        result = ResultService.create_or_update_result(user_id, diagnostic_id, autism_score)
        
        return jsonify({'result_id': result.id, 'autism_score': autism_score}), 200
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
@jwt_required()
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

    user_id = get_jwt_identity()

    try:
        autism_score = combined_analysis(image_path, video_path, questionnaire_answers)
        
        # Crear o actualizar el resultado en la base de datos
        diagnostic_id = DiagnosticService.create_diagnostic(user_id)  # O define cómo obtener el diagnostic_id
        result = ResultService.create_or_update_result(user_id, diagnostic_id, autism_score)
        
        return jsonify({'result_id': result.id, 'autism_score': autism_score}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
