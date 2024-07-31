import os
from flask import Blueprint, request, jsonify
from app.services.resultService import get_autism_score

results_bp = Blueprint('results', __name__, url_prefix='/results')

@results_bp.route('/<int:diagnostic_id>/autism_score', methods=['GET'])
def get_autism_score_route(diagnostic_id):
    try:
        autism_score = get_autism_score(diagnostic_id)
        if autism_score is not None:
            return jsonify({"autism_score": autism_score}), 200
        else:
            return jsonify({"error": "No se encontró el diagnóstico"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500