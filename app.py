import webbrowser
from __init__ import create_app
import os

app = create_app()


# Chạy ứng dụng Flask
def run_app():
    # Lấy host và port từ biến môi trường hoặc sử dụng giá trị mặc định
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = int(os.getenv('FLASK_PORT', 5000))

    # URL để mở trình duyệt
    url = f"http://{host}:{port}/"
    print(f"Starting Flask server... Open {url} in your browser.")

    # Mở trình duyệt tự động
    webbrowser.open(url)

    # Chạy ứng dụng Flask
    try:
        app.run(host=host, port=port, debug=True, use_reloader=True)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    run_app()