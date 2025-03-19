from flask import Flask
from dotenv import load_dotenv
import os
import logging

def create_app():

    """Khởi tạo Flask app"""
    load_dotenv()

    # Cấu hình logging
    logging.basicConfig(
        filename="logs/app.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    app = Flask(__name__, static_folder='static')

    # Đăng ký blueprint
    from routes import routes
    app.register_blueprint(routes, url_prefix="/")

    return app
