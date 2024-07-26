from app.models import db, Diagnostic

class DiagnosticService:
    @staticmethod
    def create_diagnostic(user_id, scan_type):
        if scan_type not in ['video', 'image']:
            raise ValueError("Invalid scan type")
        
        new_diagnostic = Diagnostic(
            user_id=user_id,
            diagnostic_type=scan_type,
            created_at=db.func.current_timestamp()
        )
        
        db.session.add(new_diagnostic)
        db.session.commit()
        return new_diagnostic

    @staticmethod
    def update_diagnostic(diagnostic_id, video_id=None, image_id=None, questionnaire_id=None, result_id=None):
        diagnostic = Diagnostic.query.get(diagnostic_id)
        if not diagnostic:
            raise ValueError("Diagnostic not found")
        
        if video_id and diagnostic.diagnostic_type == 'video':
            diagnostic.video_id = video_id
        elif image_id and diagnostic.diagnostic_type == 'image':
            diagnostic.image_id = image_id
        
        if questionnaire_id:
            diagnostic.questionnaire_id = questionnaire_id
        
        if result_id:
            diagnostic.result_id = result_id
        
        db.session.commit()
        return diagnostic
    
    @staticmethod
    def get_diagnostic(diagnostic_id):
        diagnostic = Diagnostic.query.get(diagnostic_id)
        if not diagnostic:
            raise ValueError("Diagnostic not found")
        return diagnostic