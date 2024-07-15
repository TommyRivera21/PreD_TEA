from flask import Flask
from .auth import auth_bp
from .upload import upload_bp
from .questionnaire import questionnaire_bp
from .results import results_bp
from .home import home_bp
from .diagnostic import diagnostic_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(diagnostic_bp, url_prefix='/diagnostic')
    app.register_blueprint(home_bp, url_prefix='/')
    app.register_blueprint(questionnaire_bp, url_prefix='/questionnaire')
    app.register_blueprint(results_bp, url_prefix='/results')
    app.register_blueprint(upload_bp, url_prefix='/upload')

    return app
