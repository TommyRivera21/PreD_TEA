import datetime
from app.models import Result, Diagnostic
from app import db

def create_result(user_id, diagnostic_id, autism_score=None, image_path=None, video_path=None, qa_pairs=None):
    try:
        result = Result(
            user_id=user_id,
            diagnostic_id=diagnostic_id,
            autism_score=autism_score,
            image_path=image_path,
            video_path=video_path,
            qa_pairs=qa_pairs,
            created_at=datetime.datetime.now()
        )
        db.session.add(result)
        db.session.commit()
        return result
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Error creating result: {e}")

def update_diagnostic_with_results(diagnostic_id, image_path=None, video_path=None, qa_pairs=None, autism_score=None):
    try:
        diagnostic = Diagnostic.query.get(diagnostic_id)
        if not diagnostic:
            raise ValueError(f"No diagnostic found with ID {diagnostic_id}")
        
        if image_path:
            diagnostic.image_path = image_path
        if video_path:
            diagnostic.video_path = video_path
        if qa_pairs:
            diagnostic.qa_pairs = qa_pairs
        if autism_score is not None:
            diagnostic.autism_score = autism_score
        
        db.session.commit()
        return diagnostic
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Error updating diagnostic: {e}")

def get_results_by_user(user_id):
    try:
        results = Result.query.filter_by(user_id=user_id).all()
        return results
    except Exception as e:
        raise RuntimeError(f"Error retrieving results: {e}")
