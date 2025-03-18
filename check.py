import torch
from hybrid_model import HybridResNetViTDistilBERT  # Import class mô hình của bạn

# Load checkpoint
checkpoint_path = "D:/shoe_classifier_app/modelss/best_model.pth"
checkpoint = torch.load(checkpoint_path, map_location="cpu")

# Tạo instance mô hình
model_hybrid = HybridResNetViTDistilBERT(num_classes=4)

# Lấy danh sách các keys từ mô hình hiện tại
model_keys = set(model_hybrid.state_dict().keys())

# Lấy danh sách các keys từ checkpoint
checkpoint_keys = set(checkpoint.keys())

# So sánh
missing_keys = model_keys - checkpoint_keys
extra_keys = checkpoint_keys - model_keys

print("Missing keys in checkpoint:", missing_keys)
print("Extra keys in checkpoint:", extra_keys)

# Nếu có missing_keys, cần kiểm tra lại checkpoint hoặc cập nhật mô hình
