import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv

# Load biến môi trường
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Cấu hình logging
logging.basicConfig(
    filename="logs/chatbot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Kiểm tra API Key
if not GEMINI_API_KEY:
    logging.warning("GEMINI_API_KEY is missing. Chatbot feature will be disabled.")
    chatbot_enabled = False
else:
    genai.configure(api_key=GEMINI_API_KEY)
    chatbot_enabled = True

# Hàm gửi câu hỏi đến Gemini API
def ask_chatbot(user_input: str) -> str:
    if not chatbot_enabled:
        return "Chatbot is disabled due to missing API key."

    try:
        model_gemini = genai.GenerativeModel("gemini-2.0-flash")
        response = model_gemini.generate_content(user_input)
        reply = response.text if hasattr(response, 'text') and response.text else "No response from Gemini API."
        return reply
    except Exception as e:
        logging.error(f"Gemini API error: {e}")
        return "Error: Chatbot unavailable."
