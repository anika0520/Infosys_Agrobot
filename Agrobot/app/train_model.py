import tensorflow as tf
from tensorflow.keras import layers
import numpy as np
from sklearn.model_selection import train_test_split
import os
import logging

# Suppress TensorFlow warnings for cleaner output
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # 0 = all logs, 1 = filter INFO, 2 = filter WARNING, 3 = filter ERROR
logging.getLogger('tensorflow').setLevel(logging.ERROR)

# Dataset directory
dataset_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dataset')
image_size = (128, 128)
batch_size = 16

# Load dataset
try:
    dataset = tf.keras.preprocessing.image_dataset_from_directory(
        dataset_dir,
        labels='inferred',
        label_mode='categorical',
        image_size=image_size,
        batch_size=batch_size,
        shuffle=True
    )
except Exception as e:
    print(f"Error loading dataset: {e}")
    print("Ensure dataset directory exists and contains subfolders with images.")
    exit(1)

# Store class names before mapping
class_names = dataset.class_names
print("Class names:", class_names)

# Data augmentation
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.2),
    layers.RandomZoom(0.2),
    layers.RandomBrightness(0.2),
    layers.RandomContrast(0.2)
])

# Apply augmentation and preprocessing
def preprocess(image, label):
    image = data_augmentation(image)
    image = image / 255.0  # Normalize to [0, 1]
    return image, label

dataset = dataset.map(preprocess)

# Convert to numpy for splitting
images = []
labels = []
for img, lbl in dataset:
    images.append(img.numpy())
    labels.append(lbl.numpy())
images = np.concatenate(images)
labels = np.concatenate(labels)

# Check dataset size
print(f"Total images: {len(images)}, Classes: {len(class_names)}")

# Verify class balance
unique, counts = np.unique(labels.argmax(axis=1), return_counts=True)
print("Class distribution:", dict(zip(class_names, counts)))

# Split
x_train, x_test, y_train, y_test = train_test_split(
    images, labels, test_size=0.2, random_state=42, stratify=labels.argmax(axis=1)
)

# Build model
model = tf.keras.Sequential([
    layers.Input(shape=(128, 128, 3)),
    layers.Conv2D(32, (3, 3), activation='relu', padding='same'),
    layers.MaxPooling2D(2, 2),
    layers.Conv2D(64, (3, 3), activation='relu', padding='same'),
    layers.MaxPooling2D(2, 2),
    layers.Conv2D(128, (3, 3), activation='relu', padding='same'),
    layers.MaxPooling2D(2, 2),
    layers.Flatten(),
    layers.Dense(256, activation='relu'),
    layers.Dropout(0.5),
    layers.Dense(128, activation='relu'),
    layers.Dropout(0.3),
    layers.Dense(len(class_names), activation='softmax')
])

# Compile
model.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Early stopping
early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True
)

# Train
history = model.fit(
    x_train, y_train,
    epochs=20,
    batch_size=batch_size,
    validation_data=(x_test, y_test),
    callbacks=[early_stopping]
)

# Evaluate
loss, acc = model.evaluate(x_test, y_test)
print(f"Test Accuracy: {acc:.4f}")

# Save
model_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'model.h5')
model.save(model_path)
print(f"Model saved to {model_path}")
