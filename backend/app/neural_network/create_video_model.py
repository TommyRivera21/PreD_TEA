import sys
import os
import tensorflow as tf
import numpy as np
from tensorflow.keras.models import Sequential  # type: ignore
from tensorflow.keras.layers import Dense, LSTM, TimeDistributed, Flatten, Input  # type: ignore
from tensorflow.keras.preprocessing.image import ImageDataGenerator  # type: ignore
from tensorflow.keras.callbacks import TensorBoard # type: ignore
from datetime import datetime
from tensorflow.keras.metrics import Precision, Recall  # type: ignore

# Añadir el directorio raíz al PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from app.config import Config

# Directorios de datos
TRAINING_DATA_DIR = os.path.join(Config.TRAINING_DATA_DIR)
VALIDATION_DATA_DIR = os.path.join(Config.VALIDATION_DATA_DIR)

# Parámetros de entrenamiento
IMG_HEIGHT = 64
IMG_WIDTH = 64
BATCH_SIZE = 16
NUM_FRAMES = 10
EPOCHS = 50

def create_video_model(num_frames, img_height, img_width, num_channels):
    model = Sequential([
        Input(shape=(num_frames, img_height, img_width, num_channels)),
        TimeDistributed(Flatten()),
        LSTM(128, return_sequences=False),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001), 
                  loss='binary_crossentropy', 
                  metrics=['accuracy', Precision(), Recall()])
    model.summary()
    return model

def load_and_preprocess_data(data_generator, num_frames, img_height, img_width):
    while True:
        batch_x, batch_y = next(data_generator)
        total_images = batch_x.shape[0]
        print(f"Total images in batch: {total_images}")

        if total_images < num_frames:
            continue

        remainder = total_images % num_frames
        if remainder != 0:
            batch_x = batch_x[:total_images - remainder]
            batch_y = batch_y[:total_images - remainder]

        batch_x = batch_x.reshape(-1, num_frames, img_height, img_width, 3)
        batch_y_seq = np.array([np.mean(batch_y[i * num_frames:(i + 1) * num_frames]) for i in range(batch_x.shape[0])])

        print(f"Batch X shape: {batch_x.shape}")
        print(f"Batch Y shape: {batch_y_seq.shape}")

        yield batch_x, batch_y_seq

def check_data_generator(data_generator):
    batch_x, batch_y = next(data_generator)
    print("Sample image shape:", batch_x[0].shape)
    print("Sample label:", batch_y[0])
    print("Batch X shape:", batch_x.shape)
    print("Batch Y shape:", batch_y.shape)

def train_model(model, train_generator, validation_generator, train_steps_per_epoch, validation_steps_per_epoch, epochs):
    # Configuración de TensorBoard
    tensorboard_callback = TensorBoard(log_dir=f'{Config.TENSORBOARD_LOG_DIR}/{datetime.now().strftime("%Y%m%d-%H%M%S")}', 
                                       histogram_freq=1)

    for epoch in range(epochs):
        print(f"Iniciando epoch {epoch+1}/{epochs}")
        try:
            history = model.fit(
                train_generator,
                steps_per_epoch=train_steps_per_epoch,
                epochs=1,  # Entrenando epoch a la vez
                validation_data=validation_generator,
                validation_steps=validation_steps_per_epoch,
                callbacks=[tensorboard_callback]
            )
            print(f"Epoch {epoch+1} completado")
            print("Train Loss:", history.history['loss'][-1])
            print("Train Accuracy:", history.history['accuracy'][-1])
            print("Train Precision:", history.history['precision'][-1])
            print("Train Recall:", history.history['recall'][-1])

        except KeyboardInterrupt:
            print("Interrupción del entrenamiento")
            break

if __name__ == "__main__":
    num_channels = 3

    video_model = create_video_model(NUM_FRAMES, IMG_HEIGHT, IMG_WIDTH, num_channels)
    
    os.makedirs(Config.MODEL_DIR, exist_ok=True)
    os.makedirs(Config.TENSORBOARD_LOG_DIR, exist_ok=True)  # Crear directorio para TensorBoard
    
    datagen = ImageDataGenerator(rescale=1./255)
    
    train_data_generator = datagen.flow_from_directory(
        directory=TRAINING_DATA_DIR,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE * NUM_FRAMES,
        class_mode='binary',
        shuffle=True
    )
    
    validation_data_generator = datagen.flow_from_directory(
        directory=VALIDATION_DATA_DIR,
        target_size=(IMG_HEIGHT, IMG_WIDTH),
        batch_size=BATCH_SIZE * NUM_FRAMES,
        class_mode='binary',
        shuffle=True
    )

    # Verificar los datos del generador
    check_data_generator(train_data_generator)
    
    train_generator = load_and_preprocess_data(train_data_generator, NUM_FRAMES, IMG_HEIGHT, IMG_WIDTH)
    validation_generator = load_and_preprocess_data(validation_data_generator, NUM_FRAMES, IMG_HEIGHT, IMG_WIDTH)
    
    train_steps_per_epoch = train_data_generator.samples // (BATCH_SIZE * NUM_FRAMES)
    validation_steps_per_epoch = validation_data_generator.samples // (BATCH_SIZE * NUM_FRAMES)

    print("Num CPUs Available: ", len(tf.config.list_physical_devices('CPU')))
    
    # Ejecutar la función de entrenamiento
    train_model(video_model, train_generator, validation_generator, train_steps_per_epoch, validation_steps_per_epoch, EPOCHS)
    
    model_path = os.path.join(Config.MODEL_DIR, 'video_model.keras')
    video_model.save(model_path)
    
    print(f"Modelo de video guardado exitosamente en {model_path}")