from app.models import db, Result
from sqlalchemy.exc import SQLAlchemyError
class ResultService:
    @staticmethod
    def create_or_update_result(user_id, diagnostic_id, autism_score):
        try:
            result = Result.query.filter_by(user_id=user_id, diagnostic_id=diagnostic_id).first()
            
            if not result:
                result = Result(user_id=user_id, diagnostic_id=diagnostic_id, autism_score=autism_score)
                db.session.add(result)
            else:
                result.autism_score = autism_score
            
            db.session.commit()
            return result
        except SQLAlchemyError as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_result(diagnostic_id):
        return Result.query.filter_by(diagnostic_id=diagnostic_id).first()