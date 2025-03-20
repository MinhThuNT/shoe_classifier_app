# XAI-KICKVISION: EXPLAINABLE AI-DRIVEN MULTIMODAL FOOTWEAR RECOGNITION USING IMAGE-TEXT FUSION

## Giới thiệu

Dự án **shoe_classifier_app** cho phép người dùng tải ảnh giày lên để **phân loại (Classification)** và hiển thị kết quả **Grad-CAM** giúp trực quan hóa các vùng quan trọng trong ảnh. Ngoài ra, ứng dụng còn tích hợp một **Chatbot** hỗ trợ người dùng hỏi đáp về các loại giày.

## Tính năng chính

1. **Phân loại giày**  
   - Upload ảnh giày và nhận kết quả phân loại dựa trên mô hình hybrid(ResNet + ViT-tini + DistilBERT).  
   - Xem kết quả phân loại trực tiếp trên giao diện.

2. **Grad-CAM**  
   - Hiển thị vùng trọng tâm mà mô hình sử dụng để phân loại.  
   - Giúp người dùng hiểu rõ hơn cách mô hình “nhìn” vào ảnh.

3. **Chatbot**  
   - Chatbot tích hợp, cho phép đặt câu hỏi liên quan đến giày.  
   - Sử dụng mô hình NLP để phản hồi.

4. **Lưu trữ log**  
   - Thư mục `logs` chứa file `app.log` để ghi lại các sự kiện, lỗi (nếu có).

## Cấu trúc thư mục

```plaintext
shoe_classifier_app
├── logs
│   └── app.log                          # Log file của ứng dụng
├── models
│   ├── tokenizer                        # Thư mục/binary chứa tokenizer
│   ├── best_model.pth                   # Mô hình phân loại giày HybridResNetViTDistilBERT
│   └── distilbert_text_classifier.pth   # Mô hình xử lý mô tả người dùng DistilBERTClassifier
├── static
│   ├── scripts.js                       # File JavaScript xử lý sự kiện
│   └── styles.css                       # File CSS cho giao diện
├── templates
│   └── index.html                       # Giao diện chính của ứng dụng
├── venv                                 # Môi trường ảo (nếu có)
├── .env                                 # File cấu hình biến môi trường
├── .gitignore                           # Các file/thư mục bỏ qua khi đẩy lên Git
├── app.py                               # File chính chạy ứng dụng Flask
├── chatbot.py                           # Xử lý logic chatbot
├── check_checkpoint.py                  # Kiểm tra checkpoint của mô hình
├── grad_cam.py                          # File chứa logic tạo Grad-CAM
├── models.py                            # Các hàm load mô hình
├── requirements.txt                     # Danh sách các thư viện Python cần cài đặt
├── routes.py                            # Định nghĩa route Flask
├── utils.py                             # Chứa hàm phụ trợ, tiện ích
└── README.md                            # File hướng dẫn & thông tin dự án
```

## Hướng dẫn cài đặt
1. **Clone dự án**

```bash
git clone https://github.com/MinhThuNT/shoe_classifier_app.git
cd shoe_classifier_app
```

2. **Tạo môi trường ảo (tùy chọn nhưng khuyến khích)**

```bash
python -m venv venv
venv\Scripts\activate
```

3. **Cài đặt thư viện**

```bash
pip install -r requirements.txt
```

4. **Cấu hình biến môi trường (nếu cần)**

* Tạo file .env (nếu chưa có) và thêm các thông tin như SECRET_KEY, đường dẫn mô hình, v.v.

## Cách chạy ứng dụng

1. **Chạy Flask app**

```bash
python app.py
```

2. **Truy cập trình duyệt**

* Mở trình duyệt và truy cập http://127.0.0.1:5000 (hoặc địa chỉ tương tự). 
* Hoặc chạy app.py sẽ mở trình duyệt tự động.

## Hướng dẫn sử dụng

1. **Upload ảnh để phân loại:**

* Chọn ảnh giày từ máy tính.
* Nhấn nút "Classify" để xem kết quả phân loại.
* Nhấn "Grad-CAM" để hiển thị vùng trọng tâm mô hình sử dụng.

2. **Chatbot:**

* Nhập câu hỏi về giày vào hộp chat.
* Nhấn "Send" để nhận phản hồi từ chatbot.

3. **Reset:**

* Nút "Reset" xóa ảnh, mô tả, kết quả phân loại và Grad-CAM.
* Nút "Reset Chat" để xóa và khởi động lại đoạn chat.

## Công nghệ sử dụng

- **Backend:**  
  - **Python & Flask:** Xây dựng API và server cho ứng dụng.
  - **Gemini API:** Call API của Gemini để xử lý các tác vụ NLP, giúp chatbot phản hồi câu hỏi một cách chính xác mà không cần tích hợp các thư viện NLP nội bộ.

- **Frontend:**  
  - **HTML, CSS, JavaScript:** Tạo giao diện người dùng thân thiện và responsive.
  - **Marked.js:** Xử lý Markdown cho nội dung hiển thị trong hộp chat (nếu cần).

- **Machine Learning:**  
  - **Mô hình phân loại ảnh & Grad-CAM:** Sử dụng các mô hình học sâu (có thể dựa trên PyTorch/TensorFlow) để phân loại ảnh giày và trực quan hóa kết quả Grad-CAM.

## Hướng phát triển

* Cải thiện độ chính xác mô hình phân loại giày.
* Tích hợp nhiều loại mô hình khác nhau.
* Tăng cường khả năng tương tác của chatbot, ví dụ như gợi ý sản phẩm hoặc trả lời chuyên sâu hơn.

## Tác giả

1. Nguyễn Lê Gia Bảo - [gbaooo2407@gmail.com](mailto:gbaooo2407@gmail.com)
2. Nguyễn Thị Minh Thư - [thuntmse185043@fpt.edu.vn](mailto:thuntmse185043@fpt.edu.vn)
3. Nguyễn Cao Cường - [cuongncse184384@fpt.edu.vn](mailto:cuongncse184384@fpt.edu.vn)
4. Nguyễn Hồng Nhung - [nhungnhse185000@fpt.edu.vn](mailto:nhungnhse185000@fpt.edu.vn)

---

### Giải thích nội dung README:

1. **Giới thiệu & Tính năng chính**: Nói rõ ứng dụng làm gì, có những chức năng nào.  
2. **Cấu trúc thư mục**: Chức mã nguồn.  
3. **Hướng dẫn cài đặt & chạy**: Chi tiết các bước thiết lập môi trường, cài đặt thư viện, chạy server.  
4. **Hướng dẫn sử dụng**: Hướng dẫn thao tác cụ thể trên giao diện web.  
5. **Công nghệ sử dụng**: Liệt kê ngắn gọn các công nghệ quan trọng.  
6. **Hướng phát triển**: Tiềm năng mở rộng.  
7. **Tác giả**: Đóng góp của các thành viên trong thực hiện dự án này.

