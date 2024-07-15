from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.neural_network_service import analyze_image_and_questionnaire, analyze_video_and_questionnaire
from app.services.resultService import save_result
from app.models import Image, Result, Video, Questionnaire
from app.services.diagnosticService import DiagnosticService

results_bp = Blueprint('results', __name__, url_prefix='/results')

@results_bp.route('/analyze_image', methods=['POST'])
@jwt_required()
def analyze_image_route():
    users_id = get_jwt_identity()
    data = request.get_json()
    image_id = data.get('image_id')
    questionnaire_id = data.get('questionnaire_id')
    diagnostic_id = data.get('diagnostic_id')
    
    image = Image.query.get(image_id)
    questionnaire = Questionnaire.query.get(questionnaire_id)
    
    if not image or not questionnaire:
        return jsonify({"msg": "Image or Questionnaire not found"}), 404
    
    autism_score = analyze_image_and_questionnaire(image.image_path, questionnaire.answers)
    result = save_result(users_id=users_id, autism_score=autism_score, image_id=image_id, questionnaire_id=questionnaire_id)
    
    
    DiagnosticService.update_diagnostic(diagnostic_id, result_id=result.id)
    
    return jsonify({"result_id": result.id, "autism_score": autism_score}), 200

@results_bp.route('/analyze_video', methods=['POST'])
@jwt_required()
def analyze_video_route():
    users_id = get_jwt_identity()
    data = request.get_json()
    video_id = data.get('video_id')
    questionnaire_id = data.get('questionnaire_id')
    diagnostic_id = data.get('diagnostic_id')
    
    video = Video.query.get(video_id)
    questionnaire = Questionnaire.query.get(questionnaire_id)
    
    if not video or not questionnaire:
        return jsonify({"msg": "Video or Questionnaire not found"}), 404
    
    autism_score = analyze_video_and_questionnaire(video.video_path, questionnaire.answers)
    result = save_result(users_id=users_id, autism_score=autism_score, video_id=video_id, questionnaire_id=questionnaire_id)
    
    # Update diagnostic with result_id
    DiagnosticService.update_diagnostic(diagnostic_id, result_id=result.id)
    
    return jsonify({"result_id": result.id, "autism_score": autism_score}), 200

@results_bp.route('/results', methods=['GET'])
@jwt_required()
def get_results():
    users_id = get_jwt_identity()
    results = Result.query.filter_by(users_id=users_id).all()
    results_list = [{"id": result.id, "autism_score": result.autism_score, "created_at": result.created_at} for result in results]
    return jsonify(results_list), 200
