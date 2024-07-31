from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import numpy as np
from app.services.fileService import save_image, save_video
from app.models import Diagnostic, db
from app.services.neural_network_service import image_analysis_service, calculate_average_score, video_analysis_service
from app.services.resultService import insert_files_score_result

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

    # Ejecutar análisis para cada imagen guardada
    results = []
    for image in saved_images:
        image_path = image.image_path
        try:
            # Ejecutar análisis solo después de guardar la imagen
            result = image_analysis_service(image.id, image_path)
            # Actualizar el registro de la imagen con la puntuación de predicción
            image.image_prediction_score = result['prediction_score']
            db.session.commit()
            results.append({"image_id": image.id, "image_path": image.image_path, "result": result})
        except Exception as e:
            print(f"Error analyzing image {image.id}: {e}")

    # Calcular el promedio de las predicciones y actualizar el campo `files_score`
    average_score = calculate_average_score(diagnostic_id)
    insert_files_score_result(diagnostic_id, user_id, average_score)

    return jsonify(results), 201

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

    # Ejecutar análisis para el video guardado
    video_path = video.video_path
    try:
        result = video_analysis_service(video.id, video_path)
        # Actualizar el registro del video con la puntuación de predicción
        video.video_prediction_score = result['prediction_score']
        db.session.commit()
        return jsonify({"video_id": video.id, "video_path": video.video_path, "result": result}), 201
    except Exception as e:
        print(f"Error analyzing video {video.id}: {e}")
        return jsonify({"error": str(e)}), 500