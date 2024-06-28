from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Users, AuthToken, db

def login(email, password):
    users = Users.query.filter_by(email=email).first()
    if users and check_password_hash(users.password, password):
        token = generate_password_hash(users.email + str(users.created_at))
        auth_token = AuthToken(users_id=users.id, token=token)
        db.session.add(auth_token)
        db.session.commit()
        return {
            'token': token,
            'user': users.to_dict()
        }
    return None

def register(name, email, password):
    hashed_password = generate_password_hash(password)
    new_users = Users(name=name, email=email, password=hashed_password)
    db.session.add(new_users)
    db.session.commit()
    return new_users

def logout(token):
    AuthToken.query.filter_by(token=token).delete()
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
