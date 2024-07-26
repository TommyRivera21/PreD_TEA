from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.fileService import save_image, save_video
from app.models import Diagnostic, Questionnaire
from app.services.diagnosticService import DiagnosticService
from app.services.neural_network_service import analyze_image_and_questionnaire, analyze_video_and_questionnaire

upload_bp = Blueprint('upload', __name__, url_prefix='/upload')

@upload_bp.route('/image', methods=['POST'])
@jwt_required()
def upload_image():
    user_id = get_jwt_identity()
    diagnostic_id = request.form.get('diagnostic_id')

    if not diagnostic_id:
        return jsonify({"msg": "Diagnostic ID is required"}), 400

    try:
        diagnostic_id = int(diagnostic_id)
    except ValueError:
        return jsonify({"msg": "Invalid diagnostic ID"}), 400

    diagnostic = Diagnostic.query.filter_by(id=diagnostic_id, user_id=user_id).first()
    if not diagnostic:
        return jsonify({"msg": "Invalid diagnostic ID"}), 400

    if 'image' not in request.files:
        return jsonify({"msg": "No image part"}), 400

    files = request.files.getlist('image')

    if len(files) == 0:
        return jsonify({"msg": "No files selected"}), 400

    saved_images = save_image(files, user_id, diagnostic_id)

    # Actualizar el diagnóstico con el ID de la imagen
    DiagnosticService.update_diagnostic(diagnostic_id, image_id=saved_images[0].id)

    # Obtener las respuestas del cuestionario
    questionnaire = Questionnaire.query.filter_by(diagnostic_id=diagnostic_id).first()
    if questionnaire:
        questionnaire_answers = questionnaire.qa_pairs
    else:
        questionnaire_answers = {}

    # Ejecutar análisis para cada imagen guardada
    for image in saved_images:
        image_path = image.image_path
        try:
            # Llamar a la función que analiza la imagen y el cuestionario
            result = analyze_image_and_questionnaire(image_path, questionnaire_answers)
            print(f"Resultado del análisis de la imagen {image.id}: {result}")
        except Exception as e:
            print(f"Error analyzing image {image.id}: {e}")

    response_data = [{"image_id": image.id, "image_path": image.image_path} for image in saved_images]
    return jsonify(response_data), 201


@upload_bp.route('/video', methods=['POST'])
@jwt_required()
def upload_video():
    user_id = get_jwt_identity()
    diagnostic_id = request.form.get('diagnostic_id')

    if not diagnostic_id:
        return jsonify({"msg": "Diagnostic ID is required"}), 400

    try:
        diagnostic_id = int(diagnostic_id)
    except ValueError:
        return jsonify({"msg": "Invalid diagnostic ID"}), 400

    diagnostic = Diagnostic.query.filter_by(id=diagnostic_id, user_id=user_id).first()
    if not diagnostic:
        return jsonify({"msg": "Invalid diagnostic ID"}), 400

    if 'video' not in request.files:
        return jsonify({"msg": "No video part"}), 400

    file = request.files['video']
    if file.filename == '':
        return jsonify({"msg": "No selected file"}), 400

    video = save_video(file, user_id, diagnostic_id)

    # Actualizar el diagnostic con el ID del video
    DiagnosticService.update_diagnostic(diagnostic_id, video_id=video.id)

    # Ejecutar análisis para el video guardado
    video_path = video.video_path
    # Llamar a la función que analiza el video y el cuestionario
    # Asegúrate de que tengas las respuestas del cuestionario disponibles
    questionnaire_answers = {}  # Deberás obtener las respuestas del cuestionario de alguna manera
    analyze_video_and_questionnaire(video_path, questionnaire_answers)

    response_data = {"video_id": video.id, "video_path": video.video_path}
    return jsonify(response_data), 201
