import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array  # type: ignore
import numpy as np


img_height, img_width = 28, 28
batch_size = 20
num_classes = 5

train_datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.15,
    zoom_range=0.2,
    fill_mode="nearest",
)

val_datagen = ImageDataGenerator(rescale=1.0 / 255)

train_dir = "data/train"
val_dir = "data/validation"

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(img_height, img_width),
    color_mode="grayscale",
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

model = tf.keras.models.Sequential(
    [
        tf.keras.layers.Conv2D(
            16, (3, 3), activation="relu", input_shape=(img_height, img_width, 1)
        ),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(32, (3, 3), activation="relu"),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(64, activation="relu", name="embedding"),
        tf.keras.layers.Dense(num_classes, activation="softmax"),
    ]
)

model.compile(
    optimizer=tf.keras.optimizers.Adam(),
    loss="categorical_crossentropy",
    metrics=["accuracy"],
)

model.summary()

epochs = 50
history = model.fit(
    train_generator, epochs=epochs, validation_data=validation_generator
)

model.save("trained_model.keras")


def predict_label(image_path):
   
    img = load_img(
        image_path, target_size=(img_height, img_width), color_mode="grayscale"
    )
    img_array = img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    predicted_class_index = np.argmax(prediction[0])

    label_map = {v: k for k, v in train_generator.class_indices.items()}
    predicted_label = label_map.get(predicted_class_index, "Unknown")
    return predicted_label


predicted = predict_label("data/shape.png")
print("Predicted label:", predicted)

label_map = train_generator.class_indices
print(label_map)
