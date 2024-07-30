from app.models import db, Questionnaire
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict
from app.services.neural_network_service import questionnaire_analysis_service
import json

class QuestionnaireService:
    @staticmethod
    def submit_questionnaire(user_id: int, qa_pairs: List[Dict[str, str]], diagnostic_id: int) -> int:
        if isinstance(qa_pairs, str):
            try:
                qa_pairs = json.loads(qa_pairs)
            except json.JSONDecodeError:
                raise ValueError("qa_pairs debe ser una lista de diccionarios válida o una cadena JSON válida")

        if not isinstance(qa_pairs, list) or not all(isinstance(pair, dict) and 'question' in pair and 'answer' in pair for pair in qa_pairs):
            raise ValueError("qa_pairs debe ser una lista de diccionarios con claves 'question' y 'answer'")

        valid_answers = {'Siempre', 'Generalmente', 'A veces', 'Rara vez', 'Nunca'}
        for pair in qa_pairs:
            if pair['answer'] not in valid_answers:
                raise ValueError(f"Respuesta no válida: {pair['answer']}")

        try:
            questionnaire = Questionnaire(
                user_id=user_id,
                diagnostic_id=diagnostic_id,
                qa_pairs=json.dumps(qa_pairs),  # Asegúrate de que qa_pairs esté en formato JSON
                questionnaire_prediction_score=None  # Inicialmente NULL
            )
            
            db.session.add(questionnaire)
            db.session.commit()

            # Devuelve el ID del cuestionario creado para su posterior análisis
            return questionnaire.id
        except ValueError as e:
            db.session.rollback()
            raise RuntimeError(f"Error al procesar el cuestionario: {e}")
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RuntimeError(f"Error al guardar el cuestionario en la base de datos: {e}")
        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Error inesperado: {e}")

    @staticmethod
    def update_questionnaire_score(questionnaire_id: int, score: float):
        try:
            questionnaire = Questionnaire.query.get(questionnaire_id)
            if questionnaire:
                questionnaire.questionnaire_prediction_score = score
                db.session.commit()
            else:
                raise ValueError("Cuestionario no encontrado")
        except SQLAlchemyError as e:
            db.session.rollback()
            raise RuntimeError(f"Error al actualizar la puntuación del cuestionario en la base de datos: {e}")
        except Exception as e:
            db.session.rollback()
            raise RuntimeError(f"Error inesperado al actualizar la puntuación del cuestionario: {e}")