from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
from . import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='users')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    videos = db.relationship('Video', back_populates='user')
    images = db.relationship('Image', back_populates='user')
    questionnaires = db.relationship('Questionnaire', back_populates='user')
    diagnostics = db.relationship('Diagnostic', back_populates='user')
    results = db.relationship('Result', back_populates='user')
    auth_tokens = db.relationship('AuthToken', back_populates='user')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }

class Diagnostic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    diagnostic_type = db.Column(db.String(50), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=True)

    images = db.relationship('Image', back_populates='diagnostic', cascade="all, delete-orphan")
    video = db.relationship('Video', back_populates='diagnostic', uselist=False, cascade="all, delete-orphan")
    questionnaire = db.relationship('Questionnaire', back_populates='diagnostic', uselist=False, cascade="all, delete-orphan")
    user = db.relationship('Users', back_populates='diagnostics')
    result = db.relationship('Result', back_populates='diagnostic', uselist=False, cascade="all, delete-orphan")

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    diagnostic_id = db.Column(db.Integer, ForeignKey('diagnostic.id'), nullable=False)
    video_prediction_score = db.Column(db.Float, nullable=False)
    video_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    diagnostic = db.relationship('Diagnostic', back_populates='video')
    user = db.relationship('Users', back_populates='videos')

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    diagnostic_id = db.Column(db.Integer, ForeignKey('diagnostic.id'), nullable=False)
    image_prediction_score = db.Column(db.Float, nullable=True)
    image_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    diagnostic = db.relationship('Diagnostic', back_populates='images')
    user = db.relationship('Users', back_populates='images')

class Questionnaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    diagnostic_id = db.Column(db.Integer, ForeignKey('diagnostic.id'), nullable=False)
    questionnaire_prediction_score = db.Column(db.Float, nullable=True)
    qa_pairs = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    diagnostic = db.relationship('Diagnostic', back_populates='questionnaire')
    user = db.relationship('Users', back_populates='questionnaires')

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    diagnostic_id = db.Column(db.Integer, ForeignKey('diagnostic.id'), nullable=False)
    files_score = db.Column(db.Float, nullable=False)
    questionnaire_score = db.Column(db.Float, nullable=True)
    autism_score = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    diagnostic = db.relationship('Diagnostic', back_populates='result')
    user = db.relationship('Users', back_populates='results')

class AuthToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    user = db.relationship('Users', back_populates='auth_tokens') 

    def __repr__(self):
        return f'<AuthToken id={self.id} user_id={self.user_id}>'
