from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Diagnostic
from app.services.questionnaireService import QuestionnaireService
from app.services.neural_network_service import analyze_image_and_questionnaire, analyze_video_and_questionnaire

questionnaire_bp = Blueprint('questionnaire', __name__, url_prefix='/questionnaire')

@questionnaire_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_questionnaire():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "Invalid input, JSON data expected"}), 400
        
        diagnostic_id = data.get('diagnostic_id')
        qa_pairs = data.get('qa_pairs')

        if not diagnostic_id or not qa_pairs:
            return jsonify({"error": "Missing diagnostic_id or qa_pairs"}), 400

        current_user_id = get_jwt_identity()
        
        diagnostic = Diagnostic.query.filter_by(id=diagnostic_id, user_id=current_user_id).first()
        if not diagnostic:
            return jsonify({"error": "Invalid diagnostic ID"}), 400
        
        # Guardar el cuestionario
        new_questionnaire = QuestionnaireService.submit_questionnaire(current_user_id, qa_pairs, diagnostic_id)
        
        # Obtener rutas de las imágenes y videos asociadas al diagnóstico
        diagnostic_images = diagnostic.image if diagnostic.image else []  # Usa una lista vacía si no hay imágenes
        diagnostic_videos = diagnostic.video if diagnostic.video else []  # Usa una lista vacía si no hay videos
        
        # Realizar análisis de imágenes y videos junto con el cuestionario
        for image in diagnostic_images:
            analyze_image_and_questionnaire(image.image_path, qa_pairs)
        
        for video in diagnostic_videos:
            analyze_video_and_questionnaire(video.video_path, qa_pairs)
        
        return jsonify({
            "message": "Questionnaire submitted successfully",
            "questionnaire_id": new_questionnaire.id
        }), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
