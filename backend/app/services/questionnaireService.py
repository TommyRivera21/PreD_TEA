from app.models import db, Questionnaire

class QuestionnaireService:
    @staticmethod
    def submit_questionnaire(user_id, qa_pairs, diagnostic_id):
        new_questionnaire = Questionnaire(user_id=user_id, qa_pairs=qa_pairs, diagnostic_id=diagnostic_id)
        db.session.add(new_questionnaire)
        db.session.commit()
        return new_questionnaire
