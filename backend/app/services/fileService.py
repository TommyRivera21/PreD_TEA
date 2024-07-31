import os
from werkzeug.utils import secure_filename
from app.models import Image, Video
from app import db
from flask import current_app

def save_image(files, user_id, diagnostic_id):
    saved_images = []
    
    user_id_str = str(user_id)
    diagnostic_id_str = str(diagnostic_id)
    
    base_path = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], user_id_str, diagnostic_id_str)
    os.makedirs(base_path, exist_ok=True)
    
    for file in files:
        file_path = os.path.join(base_path, file.filename)
        file.save(file_path)
        
        # Aquí puedes calcular el `image_prediction_score` si tienes la lógica
        # Si no, puedes establecerlo en None o en un valor predeterminado si tu modelo lo permite
        image_prediction_score = None
        
        # Crear y guardar el registro en la base de datos
        image = Image(user_id=user_id, diagnostic_id=diagnostic_id, image_path=file_path, image_prediction_score=image_prediction_score)
        db.session.add(image)
        db.session.commit()
        saved_images.append(image)
    
    return saved_images

def save_video(file, user_id, diagnostic_id):
    try:
        os.makedirs(current_app.config['UPLOADED_VIDEOS_DEST'], exist_ok=True)
    except OSError as e:
        print(f"Error creating video directory: {e}")
        raise

    filename = secure_filename(file.filename)
    video_path = os.path.join(current_app.config['UPLOADED_VIDEOS_DEST'], filename)
    try:
        file.save(video_path)
    except Exception as e:
        print(f"Error saving video {filename}: {e}")
        raise
    
    video = Video(user_id=user_id, video_path=video_path, diagnostic_id=int(diagnostic_id), video_prediction_score=0.0)
    db.session.add(video)
    db.session.commit()
    
    return video
