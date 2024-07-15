from app.models import db, Questionnaire

class QuestionnaireService:
    @staticmethod
    def submit_questionnaire(users_id, answers, diagnostic_id):
        new_questionnaire = Questionnaire(users_id=users_id, answers=answers, diagnostic_id=diagnostic_id)
        db.session.add(new_questionnaire)
        db.session.commit()
        return new_questionnaire
