from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.fileService import save_image, save_video

upload_bp = Blueprint('upload', __name__, url_prefix='/upload')

@upload_bp.route('/upload/image', methods=['POST'])
@jwt_required()
def upload_image():
    user_id = get_jwt_identity()
    if 'image' not in request.files:
        return jsonify({"msg": "No image part"}), 400
    file = request.files['image']
    if file.filename == '':
        return jsonify({"msg": "No selected file"}), 400
    image = save_image(file, user_id)
    return jsonify({"image_id": image.id, "image_path": image.image_path}), 201

@upload_bp.route('/upload/video', methods=['POST'])
@jwt_required()
def upload_video():
    user_id = get_jwt_identity()
    if 'video' not in request.files:
        return jsonify({"msg": "No video part"}), 400
    file = request.files['video']
    if file.filename == '':
        return jsonify({"msg": "No selected file"}), 400
    video = save_video(file, user_id)
    return jsonify({"video_id": video.id, "video_path": video.video_path}), 201
