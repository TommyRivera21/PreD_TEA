from flask import Blueprint, request, jsonify
from app.models import db, Questionnaire

questionnaire_bp = Blueprint('questionnaire', __name__)

@questionnaire_bp.route('/submit', methods=['POST'])
def submit_questionnaire():
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Invalid input"}), 400
    
    users_id = data.get('users_id')
    answers = data.get('answers')
    
    if not users_id or not answers:
        return jsonify({"error": "Missing user_id or answers"}), 400

    try:
        new_questionnaire = Questionnaire(users_id=users_id, answers=answers)
        db.session.add(new_questionnaire)
        db.session.commit()
        return jsonify({"message": "Questionnaire submitted successfully", "questionnaire_id": new_questionnaire.id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500