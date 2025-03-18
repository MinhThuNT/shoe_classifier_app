from torchvision import transforms
import numpy as np
import cv2
import re
import torch

def get_image_transform():
    """Trả về pipeline transform để xử lý ảnh đầu vào."""
    return transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

def overlay_heatmap(image_tensor, heatmap):
    """Overlay heatmap lên ảnh gốc."""
    image_np = image_tensor.squeeze(0).permute(1, 2, 0).cpu().numpy()
    heatmap = (heatmap - heatmap.min()) / (heatmap.max() - heatmap.min())
    heatmap_resized = cv2.resize(heatmap, (image_np.shape[1], image_np.shape[0]))
    heatmap_colored = cv2.applyColorMap((heatmap_resized * 255).astype(np.uint8), cv2.COLORMAP_JET)

    # Convert RGB -> BGR để xử lý OpenCV
    image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    image_bgr = np.uint8(image_bgr * 255)

    overlayed_image = cv2.addWeighted(image_bgr, 0.7, heatmap_colored, 0.3, 0)
    overlayed_image = cv2.cvtColor(overlayed_image, cv2.COLOR_BGR2RGB)
    return overlayed_image

def is_valid_text(text):
    """Kiểm tra xem văn bản có hợp lệ hay không (có chứa ít nhất một chữ cái hoặc số)."""
    return bool(re.search(r'[a-zA-Z0-9]', text))