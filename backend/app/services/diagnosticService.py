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
    def update_diagnostic(diagnostic_id, **kwargs):
        diagnostic = Diagnostic.query.get(diagnostic_id)
        if diagnostic:
            for key, value in kwargs.items():
                if hasattr(diagnostic, key):
                    setattr(diagnostic, key, value)
            db.session.commit()
        else:
            raise ValueError("Diagnostic not found")
    
    @staticmethod
    def get_diagnostic(diagnostic_id):
        diagnostic = Diagnostic.query.get(diagnostic_id)
        if not diagnostic:
            raise ValueError("Diagnostic not found")
        return diagnostic
