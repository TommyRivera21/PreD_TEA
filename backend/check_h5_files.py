import os
import h5py

def check_h5_file(file_path):
    try:
        with h5py.File(file_path, 'r') as f:
            print(f"Archivo {file_path} abierto correctamente.")
            print("Claves en el archivo:", list(f.keys()))
    except Exception as e:
        print(f"Error al abrir el archivo {file_path}: {e}")

# Verifica los archivos (ajusta las rutas si es necesario)
files_to_check = [
    'app/neural_network/models/image_model.h5',
    'app/neural_network/models/video_model.h5',
    'app/neural_network/models/questionnaire_model.h5'
]

for file in files_to_check:
    check_h5_file(file)
