import os
from werkzeug.utils import secure_filename
from app.models import Image, Video
from app import db
from flask import current_app

def save_image(file, user_id, diagnostic_id):
    try:
        os.makedirs(current_app.config['UPLOADED_PHOTOS_DEST'], exist_ok=True)
        os.makedirs(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], str(user_id)), exist_ok=True)
        os.makedirs(os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], str(user_id), str(diagnostic_id)), exist_ok=True)
    except OSError as e:
        print(f"Error creating directories: {e}")

    saved_images = []

    for uploaded_file in file:
        filename = secure_filename(uploaded_file.filename)
        file_path = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], str(user_id), str(diagnostic_id), filename)
        uploaded_file.save(file_path)
        
        image = Image(user_id=user_id, image_path=file_path, diagnostic_id=diagnostic_id)
        db.session.add(image)
        db.session.commit()

        saved_images.append(image)

    return saved_images

def save_video(file, user_id, diagnostic_id):
    filename = secure_filename(file.filename)
    video_path = os.path.join(current_app.config['UPLOADED_VIDEOS_DEST'], filename)
    file.save(video_path)

    video = Video(user_id=user_id, video_path=video_path, diagnostic_id=int(diagnostic_id))
    db.session.add(video)
    db.session.commit()
    
    return video