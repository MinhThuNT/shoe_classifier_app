import torch
import torch.nn as nn
import numpy as np
from torchvision import models, transforms
from transformers import DistilBertModel, DistilBertTokenizer
from timm import create_model

image_transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# Định nghĩa mô hình DistilBERTClassifier
class DistilBERTClassifier(nn.Module):
    def __init__(self):
        super(DistilBERTClassifier, self).__init__()
        self.distilbert = DistilBertModel.from_pretrained("distilbert-base-uncased")
        self.fc = nn.Linear(768, 1)  # Binary classification

    def forward(self, input_ids, attention_mask):
        outputs = self.distilbert(input_ids=input_ids, attention_mask=attention_mask)
        hidden_state = outputs.last_hidden_state[:, 0, :]
        logits = self.fc(hidden_state)
        return logits  # ✅ No sigmoid here!

# Định nghĩa mô hình HybridResNetViTDistilBERT
class HybridResNetViTDistilBERT(nn.Module):
    def __init__(self, num_classes):
        super(HybridResNetViTDistilBERT, self).__init__()

        # ResNet18
        self.resnet = models.resnet18(pretrained=True)
        self.resnet.fc = nn.Identity()
        self.resnet.avgpool = nn.AdaptiveAvgPool2d(1)

        # ViT
        self.vit = create_model('vit_tiny_patch16_224', pretrained=True)
        self.vit.head = nn.Identity()
        self.vit_fc = nn.Linear(192, 512)

        # DistilBERT
        self.distilbert = DistilBertModel.from_pretrained("distilbert-base-uncased")
        self.tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

        # Lớp fully connected cho văn bản
        self.text_fc = nn.Linear(768, 512)

        # Lớp phân loại cuối
        self.classifier = nn.Sequential(
            nn.Linear(512 + 512 + 512, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, num_classes)
        )

        self.transform = image_transform

    def forward(self, image, text=None):
        feat_resnet = self.resnet(image).view(image.size(0), -1)
        feat_vit = self.vit_fc(self.vit(image))

        if text is not None and len(text) > 0:
            inputs = self.tokenizer(
                text,
                padding='longest',
                truncation=True,
                return_tensors="pt"
            ).to(image.device)
            text_features = self.distilbert(**inputs).last_hidden_state[:, 0, :]
            feat_text = self.text_fc(text_features)
        else:
            feat_text = torch.zeros(image.size(0), 512).to(image.device)  # Giữ nguyên số chiều

        features = torch.cat((feat_resnet, feat_vit, feat_text), dim=1)
        return self.classifier(features)
