from flask import Flask, request, jsonify
import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing.image import img_to_array
import io
from PIL import Image, ImageOps
import cv2
# Khởi tạo ứng dụng Flask
app = Flask(__name__)

# Load mô hình Keras đã huấn luyện
model = tf.keras.models.load_model("./trained_model.keras")

# Danh sách nhãn mới (mapping index → class label)
class_indices = {0: "delta", 1: "lambda", 2: "om", 3: "omega", 4: "phi"}

# Hàm tiền xử lý ảnh đầu vào (Giữ đúng tỷ lệ ảnh, không bị méo)


def preprocess_image(image):
    # Chuyển ảnh sang grayscale
    image = image.convert("L")

    # Giữ tỷ lệ khi resize về 28x28
    image = ImageOps.fit(image, (28, 28), method=Image.Resampling.LANCZOS)

    # Chuyển ảnh sang numpy array
    image_array = np.array(image)

    # **Bước 1: Cân bằng độ tương phản bằng Adaptive Histogram Equalization**
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    image_array = clahe.apply(image_array)

    # **Bước 2: Chuẩn hóa ảnh về khoảng [0,1]**
    image_array = image_array / 255.0

    # **Bước 3: Thêm batch dimension**
    image_array = np.expand_dims(image_array, axis=0)  # (1, 28, 28)
    image_array = np.expand_dims(image_array, axis=-1)  # (1, 28, 28, 1)

    return image_array

# API nhận ảnh và trả về dự đoán


@app.route("/predict", methods=["POST"])
def predict():
    try:
        if "file" not in request.files:
            return jsonify({"error": "Không tìm thấy ảnh trong request!"}), 400

        file = request.files["file"]
        image = Image.open(io.BytesIO(file.read()))  # Đọc ảnh từ request
        image = preprocess_image(image)  # Tiền xử lý ảnh

        # Dự đoán với model
        prediction = model.predict(image)
        predicted_class_index = np.argmax(
            prediction[0])  # Lấy lớp có xác suất cao nhất
        predicted_label = class_indices.get(predicted_class_index, "Unknown")
        confidence = float(np.max(prediction[0]))  # Độ tin cậy của dự đoán

        return jsonify({"prediction": predicted_label, "confidence": confidence})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Chạy server Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
