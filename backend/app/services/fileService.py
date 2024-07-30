import os
from werkzeug.utils import secure_filename
from app.models import Image, Video
from app import db
from flask import current_app

def save_image(files, user_id, diagnostic_id):
    try:
        base_path = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], str(user_id), str(diagnostic_id))
        os.makedirs(base_path, exist_ok=True)
    except OSError as e:
        print(f"Error creating directories: {e}")
        raise

    saved_images = []

    for uploaded_file in files:
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join(base_path, filename)
        try:
            uploaded_file.save(file_path)
        except Exception as e:
            print(f"Error saving file {filename}: {e}")
            continue
        
        image = Image(user_id=user_id, image_path=file_path, diagnostic_id=diagnostic_id, image_prediction_score=0.0)
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
