from . import db

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='users')
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    questionnaires = db.relationship('Questionnaire', backref='user', lazy=True)
    videos = db.relationship('Video', backref='user', lazy=True)
    images = db.relationship('Image', backref='user', lazy=True)
    diagnostics = db.relationship('Diagnostic', back_populates='user', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
        }

class Video(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    video_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    diagnostic_id = db.Column(db.Integer, db.ForeignKey('diagnostic.id'), nullable=True)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image_path = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    diagnostic_id = db.Column(db.Integer, db.ForeignKey('diagnostic.id'), nullable=True)

class Questionnaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    qa_pairs = db.Column(db.JSON, nullable=False)  
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    results = db.relationship('Result', backref='questionnaire', lazy=True)
    diagnostic_id = db.Column(db.Integer, db.ForeignKey('diagnostic.id'), nullable=True)

class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=True)
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id'), nullable=False)
    autism_score = db.Column(db.Numeric(5, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    video = db.relationship('Video', backref='results', lazy=True)
    image = db.relationship('Image', backref='results', lazy=True)

class Diagnostic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    video_id = db.Column(db.Integer, db.ForeignKey('video.id'), nullable=True)
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'), nullable=True)
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('questionnaire.id'), nullable=True)
    result_id = db.Column(db.Integer, db.ForeignKey('result.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    user = db.relationship('Users', back_populates='diagnostics')

class AuthToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('Users', backref='auth_tokens', lazy=True)

    def __repr__(self):
        return f'<AuthToken id={self.id} user_id={self.user_id}>'
