import tensorflow as tf
import numpy as np
import cv2
from flask import current_app
import os

class AutismPredictionModel:
    def __init__(self, model_path):
        if not os.path.exists(model_path):
            current_app.logger.warning(f"Model file not found at {model_path}. Skipping model initialization.")
            return
        self.model = tf.keras.models.load_model(model_path)
    
    def preprocess_video(self, video_path):
        cap = cv2.VideoCapture(video_path)
        frames = []
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.resize(frame, (224, 224))
            frame = frame / 255.0
            frames.append(frame)
        cap.release()
        frames_array = np.array(frames)
        frames_array = np.expand_dims(frames_array, axis=0)
        return frames_array
    
    def preprocess_questionnaire(self, answers):
        questionnaire_data = np.array(answers).reshape(1, -1)
        return questionnaire_data
    
    def predict(self, video_path, answers):
        video_data = self.preprocess_video(video_path)
        questionnaire_data = self.preprocess_questionnaire(answers)
        prediction = self.model.predict([video_data, questionnaire_data])
        return prediction

def init_model():
    model_path = current_app.config['MODEL_PATH']
    try:
        current_app.prediction_model = AutismPredictionModel(model_path)
    except Exception as e:
        current_app.logger.warning(f"Model initialization failed: {e}")
