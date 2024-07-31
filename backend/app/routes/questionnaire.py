from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.questionnaireService import QuestionnaireService
from app.services.neural_network_service import questionnaire_analysis_service
from app.services.resultService import update_questionnaire_score_in_result

questionnaire_bp = Blueprint('questionnaire', __name__, url_prefix='/questionnaire')

@questionnaire_bp.route('/submit', methods=['POST'])
@jwt_required()
def submit_questionnaire():
    user_id = get_jwt_identity()
    data = request.get_json()
    
    diagnostic_id = data.get('diagnostic_id')
    qa_pairs = data.get('qa_pairs')
    
    if not diagnostic_id or not qa_pairs:
        return jsonify({"error": "Faltan diagnostic_id o qa_pairs"}), 400
    
    try:
        # Guardar el cuestionario
        questionnaire_id = QuestionnaireService.submit_questionnaire(user_id, qa_pairs, diagnostic_id)
        
        # Analizar el cuestionario
        questionnaire_analysis_result = questionnaire_analysis_service(questionnaire_id, qa_pairs)
        
        # Actualizar el cuestionario con el resultado del análisis
        QuestionnaireService.update_questionnaire_score(questionnaire_id, questionnaire_analysis_result['prediction_score'])

        # Guardar el resultado del análisis en la tabla Result
        update_questionnaire_score_in_result(diagnostic_id, user_id, questionnaire_analysis_result['prediction_score'])
        
        return jsonify({
            "message": "Cuestionario enviado con éxito",
            "diagnostic_id": diagnostic_id,
            "questionnaire_id": questionnaire_id,
            "analysis_result": questionnaire_analysis_result['prediction_score'],
            "notification": "Prediccion del questionnaire guardada en la tabla result"
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500