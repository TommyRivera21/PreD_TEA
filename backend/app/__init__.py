from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import logging

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    JWTManager(app)

    CORS(app)

    # Configurar el logging
    logging.basicConfig(level=logging.INFO)
    
    from .routes.auth import auth_bp
    from .routes.diagnostic import diagnostic_bp
    from .routes.home import home_bp
    from .routes.questionnaire import questionnaire_bp
    from .routes.results import results_bp
    from .routes.upload import upload_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(diagnostic_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(questionnaire_bp)
    app.register_blueprint(results_bp)
    app.register_blueprint(upload_bp)

    return app