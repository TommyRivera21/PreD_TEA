from app.models import Result
from app import db

def save_result(users_id, autism_score, video_id=None, image_id=None, questionnaire_id=None):
    result = Result(users_id=users_id, autism_score=autism_score, video_id=video_id, image_id=image_id, questionnaire_id=questionnaire_id)
    db.session.add(result)
    db.session.commit()
    return result
