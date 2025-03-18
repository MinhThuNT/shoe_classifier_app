import torch
import numpy as np
import cv2
from PIL import Image
from utils import is_valid_text, overlay_heatmap, get_image_transform

class GradCAMPP:
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None

        target_layer.register_forward_hook(self.save_activation)
        target_layer.register_backward_hook(self.save_gradient)

    def save_activation(self, module, input, output):
        self.activations = output

    def save_gradient(self, module, grad_input, grad_output):
        self.gradients = grad_output[0]

    def generate_heatmap(self, input_tensor, class_idx=None):
        self.model.zero_grad()
        output = self.model(input_tensor)
        if class_idx is None:
            class_idx = output.argmax().item()
        target = output[:, class_idx]
        target.backward()
        grads = self.gradients[0].cpu().numpy()
        activations = self.activations[0].cpu().detach().numpy()
        weights = np.mean(grads, axis=(1, 2))
        heatmap = np.sum(weights[:, None, None] * activations, axis=0)
        heatmap = np.maximum(heatmap, 0)
        heatmap = heatmap / np.max(heatmap)
        return heatmap

def predict_and_explain(image, text, model_hybrid, model_text, transform):
    transform = get_image_transform()
    image_tensor = transform(image).unsqueeze(0)

    # Kiểm tra xem có sử dụng văn bản không
    if not is_valid_text(text):
        text = ""  # Bỏ qua nếu văn bản không có ý nghĩa

    model_hybrid.eval()

    with torch.no_grad():
        outputs = model_hybrid(image_tensor, text)
        _, predicted = torch.max(outputs, 1)

    class_names = {0: 'Boots', 1: 'Sandals', 2: 'Shoes', 3: 'Slippers'}
    predicted_class = class_names.get(predicted.item(), "Unknown")

    # Grad-CAM xử lý ảnh
    target_layer = model_hybrid.resnet.layer4[-1]
    gradcam = GradCAMPP(model_hybrid, target_layer)
    heatmap = gradcam.generate_heatmap(image_tensor)

    # Xử lý hiển thị ảnh với heatmap
    overlayed_image = overlay_heatmap(image_tensor, heatmap)

    # Nếu có văn bản hợp lệ, tạo mô tả từ model_text
    text_description = ""
    if text:
        with torch.no_grad():
            text_output = model_text(text)
            text_description = text_output[0].cpu().numpy()

    return overlayed_image, predicted_class, text_description