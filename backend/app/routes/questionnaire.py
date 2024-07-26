from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.questionnaireService import QuestionnaireService
from app.services.diagnosticService import DiagnosticService

questionnaire_bp = Blueprint('questionnaire', __name__, url_prefix='/questionnaire')

@questionnaire_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_questionnaire():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    diagnostic_id = data.get('diagnostic_id')
    qa_pairs = data.get('qa_pairs')
    
    if not diagnostic_id or not qa_pairs:
        return jsonify({"error": "Missing diagnostic_id or qa_pairs"}), 400
    
    try:
        questionnaire = QuestionnaireService.submit_questionnaire(user_id, qa_pairs, diagnostic_id)
        
        # Actualizar el diagnóstico con el ID del cuestionario
        DiagnosticService.update_diagnostic(diagnostic_id, questionnaire_id=questionnaire.id)
        
        return jsonify({"message": "Questionnaire submitted successfully", "questionnaire_id": questionnaire.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
