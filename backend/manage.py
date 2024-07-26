from app import create_app, db
from flask_migrate import Migrate
from app.models import Users, Video, Image, Questionnaire, Result, Diagnostic, AuthToken
app = create_app()
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()