from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.services import login, register, logout

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login_route():
    data = request.get_json()
    user_data = login(data['email'], data['password'])
    if user_data:
        access_token = create_access_token(identity=user_data['user'].id)
        refresh_token = create_refresh_token(identity=user_data['user'].id)
        return jsonify({
            'token': access_token,
            'refreshToken': refresh_token,
            'user': user_data['user'].to_dict()  
        }), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@auth_bp.route('/register', methods=['POST'])
def register_route():
    data = request.get_json()
    user = register(data['name'], data['email'], data['password'])
    if user:
        return jsonify({'message': 'User registered successfully'}), 201
    return jsonify({'message': 'Registration failed'}), 400

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout_route():
    token = request.headers.get('Authorization').split()[1]
    logout(token)
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/current-user', methods=['GET'])
@jwt_required()
def current_user_route():
    current_user = get_jwt_identity()
    if current_user:
        return jsonify(current_user), 200
    return jsonify({'message': 'User not found'}), 404

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_token = create_access_token(identity=current_user)
    return jsonify(token=new_token), 200