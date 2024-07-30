import os
from flask import Blueprint, request, jsonify
from app.services.resultService import create_result
from app.services.fileService import save_image
from app.services.neural_network_service import image_analysis_service

results_bp = Blueprint('results', __name__, url_prefix='/results')

@results_bp.route('/average_image_prediction', methods=['POST'])
def average_image_prediction():
    try:
        image_files = request.files.getlist('images')
        if len(image_files) != 10:
            return jsonify({'error': 'Se deben proporcionar exactamente 10 imágenes'}), 400
        
        # Guardar imágenes y calcular el promedio de las predicciones
        image_paths = []
        for image_file in image_files:
            image_path = save_image(image_file)
            image_paths.append(image_path)

        # Obtener el promedio de las predicciones de las 10 imágenes
        autism_score = image_analysis_service(image_paths)
        
        # Crear un resultado en la base de datos
        result = create_result(autism_score=autism_score)

        return jsonify({'autism_score': autism_score, 'result_id': result.id}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
