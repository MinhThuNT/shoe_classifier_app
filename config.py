import os
from dotenv import load_dotenv

LOG_DIR = 'logs'
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Load biến môi trường từ .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    MODEL_PATH = os.getenv("MODEL_PATH", "app/models/hybrid_model.pth")
    TOKENIZER_PATH = os.getenv("TOKENIZER_PATH", "app/models/tokenizer")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Kiểm tra GEMINI API Key
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is missing! Please check your .env file.")
