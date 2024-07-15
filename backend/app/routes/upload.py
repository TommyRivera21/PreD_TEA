from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.fileService import save_image, save_video
from app.models import Diagnostic

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

    response_data = {"video_id": video.id, "video_path": video.video_path}
    return jsonify(response_data), 201
