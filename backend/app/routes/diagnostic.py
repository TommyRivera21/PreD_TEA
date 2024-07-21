from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.diagnosticService import DiagnosticService

diagnostic_bp = Blueprint('diagnostic', __name__, url_prefix='/diagnostic')

@diagnostic_bp.route('/create', methods=['POST'])
@jwt_required()
def create_diagnostic():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        scan_type = data.get('scanType')
        if not scan_type:
            return jsonify({"error": "Scan type is required"}), 400
        
        diagnostic = DiagnosticService.create_diagnostic(user_id, scan_type)
        return jsonify({"id": diagnostic.id, "diagnostic_type": diagnostic.diagnostic_type}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@diagnostic_bp.route('/update', methods=['POST'])
@jwt_required()
def update_diagnostic():
    try:
        data = request.get_json()
        diagnostic_id = data.get('diagnostic_id')
        video_id = data.get('video_id')
        image_id = data.get('image_id')
        questionnaire_id = data.get('questionnaire_id')
        result_id = data.get('result_id')

        if not diagnostic_id:
            return jsonify({"error": "Diagnostic ID is required"}), 400
        
        try:
            diagnostic_id = int(diagnostic_id)  
            if video_id:
                video_id = int(video_id)
            if image_id:
                image_id = int(image_id)
            if questionnaire_id:
                questionnaire_id = int(questionnaire_id)
            if result_id:
                result_id = int(result_id)
        except ValueError:
            return jsonify({"error": "Invalid ID format"}), 400

        diagnostic = DiagnosticService.update_diagnostic(diagnostic_id, video_id, image_id, questionnaire_id, result_id)
        return jsonify({"message": "Diagnostic updated successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500