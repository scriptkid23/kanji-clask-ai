import tensorflow as tf

# Set parameters
img_height, img_width = 28, 28  # Image dimensions (e.g., for MNIST-like data)
batch_size = 32
num_classes = 3  # Adjust this to the actual number of classes in your dataset

# Create an ImageDataGenerator for training with data augmentation
train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale=1.0 / 255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.15,
    zoom_range=0.2,
    fill_mode="nearest",
)

# Create an ImageDataGenerator for validation (only rescaling)
val_datagen = tf.keras.preprocessing.image.ImageDataGenerator(rescale=1.0 / 255)

# Define directories for training and validation datasets
train_dir = "data/train"
val_dir = "data/validation"

# Create generators that read images from directory
# Ensure that your directories contain one folder per class (e.g., 'circle', 'square', 'triangle')
train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(img_height, img_width),
    color_mode="grayscale",  # Use 'rgb' if your images are in color
    batch_size=batch_size,
    class_mode="categorical",
)

validation_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=(img_height, img_width),
    color_mode="grayscale",
    batch_size=batch_size,
    class_mode="categorical",
)

# Build a CNN model using TensorFlow's Keras API
model = tf.keras.models.Sequential(
    [
        tf.keras.layers.Conv2D(
            16, (3, 3), activation="relu", input_shape=(img_height, img_width, 1)
        ),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(32, (3, 3), activation="relu"),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dense(num_classes, activation="softmax"),
    ]
)

# Compile the model
model.compile(
    optimizer=tf.keras.optimizers.Adam(),
    loss="categorical_crossentropy",
    metrics=["accuracy"],
)

# Display the model summary
model.summary()

# Train the model for a number of epochs
epochs = 20
history = model.fit(
    train_generator, epochs=epochs, validation_data=validation_generator
)

# Save the trained model (use native Keras format if desired)
model.save("trained_model.keras")
