import os
from werkzeug.utils import secure_filename
from app.models import Image, Video
from app import db

def save_image(file, users_id):
    filename = secure_filename(file.filename)
    file_path = os.path.join('uploads/images/', filename)
    file.save(file_path)
    image = Image(users_id=users_id, image_path=file_path)
    db.session.add(image)
    db.session.commit()
    return image

def save_video(file, users_id):
    filename = secure_filename(file.filename)
    file_path = os.path.join('uploads/videos/', filename)
    file.save(file_path)
    video = Video(users_id=users_id, video_path=file_path)
    db.session.add(video)
    db.session.commit()
    return video
