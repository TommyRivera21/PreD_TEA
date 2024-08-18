import os
import sys
from tensorflow.keras.models import Sequential  # type: ignore
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Input  # type: ignore
from tensorflow.keras.preprocessing.image import ImageDataGenerator  # type: ignore
from tensorflow.keras.callbacks import TensorBoard  # type: ignore
from tensorflow.keras.metrics import Precision, Recall  # type: ignore
from app.config import Config

def create_image_model():
    model = Sequential([
        Input(shape=(128, 128, 3)),
        Conv2D(32, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D((2, 2)),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    # Añadir Precision y Recall como métricas
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy', Precision(), Recall()])
    return model

def train_image_model(model, train_dir, validation_dir, batch_size=32, epochs=50):
    # Verifica que las rutas existan
    assert os.path.exists(train_dir), f"La ruta de entrenamiento {train_dir} no existe."
    assert os.path.exists(validation_dir), f"La ruta de validación {validation_dir} no existe."
    
    # Preprocesamiento de datos y aumento de datos
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=40,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    validation_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(128, 128),
        batch_size=batch_size,
        class_mode='binary'
    )

    validation_generator = validation_datagen.flow_from_directory(
        validation_dir,
        target_size=(128, 128),
        batch_size=batch_size,
        class_mode='binary'
    )

    # Crear el directorio para los logs de TensorBoard
    os.makedirs(Config.TENSORBOARD_LOG_DIR, exist_ok=True)
    
    # Configurar TensorBoard callback
    tensorboard_callback = TensorBoard(
        log_dir=Config.TENSORBOARD_LOG_DIR,
        histogram_freq=1
    )

    # Entrenar el modelo
    history = model.fit(
        train_generator,
        steps_per_epoch=train_generator.samples // batch_size,
        epochs=epochs,
        validation_data=validation_generator,
        validation_steps=validation_generator.samples // batch_size,
        callbacks=[tensorboard_callback]  # Agregar el callback de TensorBoard
    )

if __name__ == "__main__":
    image_model = create_image_model()
    
    # Directorios de datos de entrenamiento y validación
    train_dir = Config.TRAINING_DATA_DIR
    validation_dir = Config.VALIDATION_DATA_DIR
    
    # Entrenar el modelo
    train_image_model(image_model, train_dir, validation_dir)
    
    # Crear el directorio si no existe
    os.makedirs(Config.MODEL_DIR, exist_ok=True)
    
    # Guardar el modelo en la ruta especificada con la nueva extensión
    model_path = os.path.join(Config.MODEL_DIR, 'image_model.keras')
    image_model.save(model_path)
    
    print(f"Modelo de imagen guardado exitosamente en {model_path}")