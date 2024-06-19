import os
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from .neural_network import init_model

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)

    load_dotenv()

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER')
    app.config['MODEL_PATH'] = os.getenv('MODEL_PATH')

    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)

    from .routes import main
    app.register_blueprint(main)

    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            app.logger.error(f"Error creating database tables: {e}")
        init_model()

    return app
