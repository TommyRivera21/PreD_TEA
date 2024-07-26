from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import AuthToken, Users, db

def login(email, password):
    user = Users.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity={'id': user.id, 'email': user.email})
        return {
            'access_token': access_token,
            'user': user  
        }
    return None

def register(name, email, password):
    hashed_password = generate_password_hash(password)
    new_user = Users(name=name, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return new_user

def logout(token):
    auth_token = AuthToken.query.filter_by(token=token).first()
    if auth_token:
        db.session.delete(auth_token)
        db.session.commit()

def getCurrentToken():
    auth_token = AuthToken.query.first()
    return auth_token.token if auth_token else None

def getCurrentUser():
    token = getCurrentToken()
    if token:
        auth_token = AuthToken.query.filter_by(token=token).first()
        if auth_token:
            return Users.query.get(auth_token.user_id)
    return None
