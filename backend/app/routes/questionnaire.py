from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Diagnostic
from app.services.questionnaireService import QuestionnaireService

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
        
        new_questionnaire = QuestionnaireService.submit_questionnaire(current_user_id, qa_pairs, diagnostic_id)
        
        return jsonify({
            "message": "Questionnaire submitted successfully",
            "questionnaire_id": new_questionnaire.id
        }), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
