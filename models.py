import torch
from transformers import DistilBertTokenizer
from hybrid_model import HybridResNetViTDistilBERT, DistilBERTClassifier

def load_models():
    # Load mô hình kết hợp hình ảnh và văn bản
    model_hybrid = HybridResNetViTDistilBERT(num_classes=4)
    checkpoint_hybrid_path = "D:/shoe_classifier_app/modelss/best_model.pth"
    try:
        checkpoint_hybrid = torch.load(checkpoint_hybrid_path, map_location=torch.device('cpu'), weights_only=True)
        model_hybrid.load_state_dict(checkpoint_hybrid["model_state_dict"])
    except Exception as e:
        raise RuntimeError(f"Lỗi khi load checkpoint hình ảnh từ {checkpoint_hybrid_path}: {e}")
    model_hybrid.eval()

    # Load mô hình văn bản
    model_text = DistilBERTClassifier()
    checkpoint_text_path = "D:/shoe_classifier_app/modelss/distilbert_text_classifier.pth"
    try:
        checkpoint_text = torch.load(checkpoint_text_path, map_location="cpu")
        model_text.load_state_dict(checkpoint_text)
    except Exception as e:
        raise RuntimeError(f"Lỗi khi load checkpoint văn bản từ {checkpoint_text_path}: {e}")
    model_text.eval()

    # Load tokenizer
    tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

    return model_hybrid, model_text, tokenizer