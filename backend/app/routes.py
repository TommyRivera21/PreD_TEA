import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.utils import secure_filename
from .models import db, User


main = Blueprint('main', __name__)

@main.route('/', methods=['GET'])
def server_status():
    return jsonify('Server is running'), 200


@main.route('/test-db', methods=['GET'])
def test_db_connection():
    try:
        # Realiza una consulta simple para probar la conexión
        user_count = db.session.query(User).count()
        return jsonify({'message': 'Database connection successful!', 'user_count': user_count}), 200
    except Exception as e:
        current_app.logger.error(f"Database connection failed: {e}")
        return jsonify({'message': 'Database connection failed!', 'error': str(e)}), 500

@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    
    new_user = User(
        name=data['name'],
        email=data['email'],
        password=hashed_password
    )
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully'}), 201

@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401
    
    access_token = create_access_token(identity=user.id)
    return jsonify({'token': access_token}), 200

@main.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify({'name': user.name, 'email': user.email}), 200

@main.route('/predict', methods=['POST'])
@jwt_required()
def predict():
    if 'video' not in request.files:
        return jsonify({'error': 'No video file provided'}), 400
    if 'answers' not in request.form:
        return jsonify({'error': 'No questionnaire answers provided'}), 400

    video = request.files['video']
    answers = request.form.getlist('answers')

    filename = secure_filename(video.filename)
    video_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    video.save(video_path)

    prediction = current_app.prediction_model.predict(video_path, answers)
    os.remove(video_path)  # Limpiar el archivo temporal

    return jsonify({'prediction': prediction.tolist()}), 200
