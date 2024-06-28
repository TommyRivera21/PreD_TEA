from app.models import db, Questionnaire

class QuestionnaireService:
    @staticmethod
    def submit_questionnaire(users_id, answers):
        new_questionnaire = Questionnaire(users_id=users_id, answers=answers)
        db.session.add(new_questionnaire)
        db.session.commit()
        return new_questionnaire
