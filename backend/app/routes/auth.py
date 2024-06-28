from flask import Blueprint, request, jsonify
from app.services import login, register, logout, getCurrentUser
from flask import Blueprint, request, jsonify
from flask_cors import CORS

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['POST'])
def login_route():
    data = request.get_json()
    users = login(data['email'], data['password'])
    if users:
        return jsonify(users), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@auth_bp.route('/register', methods=['POST'])
def register_route():
    data = request.get_json()
    users = register(data['name'], data['email'], data['password'])
    if users:
        return jsonify({'message': 'User registered successfully'}), 201
    return jsonify({'message': 'Registration failed'}), 400

@auth_bp.route('/logout', methods=['POST'])
def logout_route():
    token = request.headers.get('Authorization').split()[1]
    logout(token)
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/current-user', methods=['GET'])
def current_user_route():
    users = getCurrentUser()
    if users:
        return jsonify(users), 200
    return jsonify({'message': 'User not found'}), 404
