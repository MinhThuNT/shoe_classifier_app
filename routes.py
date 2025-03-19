import torch
import cv2
import numpy as np
import base64
from PIL import Image
from flask import Blueprint, request, jsonify, render_template
from io import BytesIO
import logging

from models import load_models
from grad_cam import predict_and_explain
from chatbot import ask_chatbot
from utils import get_image_transform, overlay_heatmap, is_valid_text

# Cấu hình logging
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Tạo Blueprint cho routes
routes = Blueprint("routes", __name__)

# Load mô hình
model_hybrid, model_text, tokenizer = load_models()
if not all([model_hybrid, model_text, tokenizer]):
    logging.error("Failed to load models properly.")
    raise RuntimeError("Failed to load models.")

@routes.route('/')
def home():
    return render_template('index.html', template_folder='templates')

@routes.route('/predict', methods=['POST'])
def predict():
    """ Nhận ảnh + văn bản, phân loại giày """
    if 'file' not in request.files:
        logging.warning("Predict: No file uploaded")
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if not file or file.filename.strip() == "":
        logging.warning("Predict: Invalid file")
        return jsonify({'error': 'Invalid request'}), 400

    text = request.form.get("text", "").strip()
    if text is None:
        text = ""

    try:
        img = Image.open(file.stream).convert("RGB")
        transform = get_image_transform()
        img_tensor = transform(img).unsqueeze(0)  # Transform ảnh đầu vào

        # Nếu văn bản không hợp lệ, chỉ dùng ảnh để phân loại
        valid_text = text if is_valid_text(text) else ""

        with torch.no_grad():
            outputs = model_hybrid(img_tensor, valid_text)
            _, predicted_class = torch.max(outputs, 1)

        class_names = {0: 'Boots', 1: 'Sandal', 2: 'Shoes', 3: 'Slippers'}
        result = {
            'prediction': class_names.get(predicted_class.item(), "Unknown"),
            'description': valid_text if valid_text else "No valid description provided."
        }

        logging.info(f"Prediction result: {result}")
        return jsonify(result)

    except Exception as e:
        logging.error(f"Prediction error: {e}")
        return jsonify({'error': 'Prediction failed'}), 500

@routes.route('/gradcam', methods=['POST'])
def gradcam():
    """ Sinh ảnh heatmap Grad-CAM """
    if 'file' not in request.files:
        logging.warning("Grad-CAM: No file uploaded")
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if not file or file.filename.strip() == "":
        logging.warning("Grad-CAM: Invalid file")
        return jsonify({'error': 'Invalid request'}), 400

    text = request.form.get("text", "").strip()
    if text is None:
        text = ""

    try:
        image = Image.open(file.stream).convert("RGB")
        transform = get_image_transform()

        # Chạy Grad-CAM
        overlayed_image, predicted_class, text_description = predict_and_explain(
            image, text, model_hybrid, model_text, transform
        )

        if overlayed_image is None:
            logging.error("Grad-CAM: Failed to generate heatmap")
            return jsonify({'error': 'Grad-CAM failed'}), 500

        # Encode ảnh heatmap thành Base64 để trả về JSON
        _, buffer = cv2.imencode('.jpg', overlayed_image)
        heatmap_base64 = base64.b64encode(buffer).decode('utf-8')

        return jsonify({
            'gradcam': heatmap_base64,
            'prediction': predicted_class,
            'description': text_description
        })

    except Exception as e:
        logging.error(f"Grad-CAM error: {e}")
        return jsonify({'error': 'Grad-CAM failed'}), 500

@routes.route('/chat', methods=['POST'])
def chat():
    """ Gửi tin nhắn đến chatbot """
    data = request.json
    user_input = data.get("message", "").strip()

    if not user_input:
        logging.warning("Chat: Empty message")
        return jsonify({"reply": "Please enter a message."}), 400

    reply = ask_chatbot(user_input)  # Gọi chatbot từ chatbot.py
    return jsonify({"reply": reply})
