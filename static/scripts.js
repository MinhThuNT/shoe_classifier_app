document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ scripts.js loaded successfully!");

    // 📌 Lấy phần tử DOM
    const elements = {
        fileInput: document.getElementById("fileInput"),
        textInput: document.getElementById("textInput"),
        sendDescBtn: document.getElementById("sendDescBtn"),
        classifyBtn: document.getElementById("classifyBtn"),
        resetBtn: document.getElementById("resetBtn"),
        gradCamBtn: document.getElementById("gradCamBtn"),
        chatInput: document.getElementById("chatInput"),
        sendBtn: document.getElementById("sendBtn"),
        chatbox: document.getElementById("chatbox"),
        resetChatBtn: document.getElementById("resetChat"),
        previewImg: document.getElementById("preview"),
        classificationResult: document.getElementById("classificationResult"),
        gradcamResult: document.getElementById("gradcamResult"),
        loadingIndicator: document.getElementById("loadingIndicator"),
        descriptionDisplay: document.getElementById("descriptionDisplay")
    };

    // Kiểm tra phần tử có tồn tại không
    Object.entries(elements).forEach(([key, value]) => {
        if (!value) console.error(`❌ Missing element: ${key}`);
    });

    // Ẩn ảnh xem trước và Grad-CAM khi chưa có file
    elements.previewImg.style.display = "none";
    elements.gradcamResult.style.display = "none";
    elements.loadingIndicator.style.display = "none";
    elements.descriptionDisplay.style.display = "none";

    // 🖼️ Hiển thị ảnh xem trước
    elements.fileInput?.addEventListener("change", function (event) {
        const file = event.target.files[0];
        if (file && file.type.startsWith("image/")) {
            const reader = new FileReader();
            reader.onload = (e) => {
                elements.previewImg.src = e.target.result;
                elements.previewImg.style.display = "block";
            };
            reader.readAsDataURL(file);
        } else {
            alert("⚠️ Please upload a valid image file.");
            elements.fileInput.value = "";
            elements.previewImg.style.display = "none";
        }
    });

    // 📝 Gửi mô tả văn bản và hiển thị bên cạnh image
    elements.sendDescBtn?.addEventListener("click", async () => {
        await sendDescription();
    });
    elements.textInput?.addEventListener("keyup", async (event) => {
        if (event.key === "Enter" && !event.shiftKey) await sendDescription();
    });

    async function sendDescription() {
        const description = elements.textInput.value.trim();
        if (!description) return;

        elements.descriptionDisplay.innerText = `📜 ${description}`;
        elements.descriptionDisplay.style.display = "block";
        elements.textInput.value = "";

        const response = await fetchData("/send_desc", { description });
        console.log(response?.response || "No response from server.");
    }

    // 🔍 Phân loại ảnh
    elements.classifyBtn?.addEventListener("click", async () => {
        await processImage("/predict", elements.classificationResult, "Classification Result: ");
    });

    // 🔄 Reset ảnh và kết quả
    elements.resetBtn?.addEventListener("click", function () {
        elements.fileInput.value = "";
        elements.textInput.value = "";
        elements.previewImg.src = "";
        elements.previewImg.style.display = "none";
        elements.classificationResult.innerText = "";
        elements.gradcamResult.src = "";
        elements.gradcamResult.style.display = "none";
        elements.descriptionDisplay.innerText = "";
        elements.descriptionDisplay.style.display = "none";
    });

    // 🔥 Hiển thị Grad-CAM
    elements.gradCamBtn?.addEventListener("click", async () => {
        await processImage("/gradcam", elements.gradcamResult, "Grad-CAM Result: ");
    });

    // 💬 Chat với chatbot
    elements.sendBtn?.addEventListener("click", async () => {
        await sendMessage(elements.chatInput.value.trim());
    });
    elements.chatInput?.addEventListener("keyup", async (event) => {
        if (event.key === "Enter" && !event.shiftKey) await sendMessage(elements.chatInput.value.trim());
    });

    async function sendMessage(message) {
        if (!message) return;
        addMessage(elements.chatbox, message, "user-msg");
        elements.chatInput.value = "";

        const response = await fetchData("/chat", { message, classification: elements.classificationResult.innerText });
        if (response && response.reply) {
            addMessage(elements.chatbox, response.reply, "bot-msg");
        } else {
            alert("⚠️ Chatbot is currently unavailable.");
        }
    }

    // 🔄 Reset chat
    elements.resetChatBtn?.addEventListener("click", function () {
        elements.chatbox.innerHTML = "";
    });

    // 🖼️ Xử lý gửi ảnh
    async function processImage(url, outputElement, prefix = "") {
        const file = elements.fileInput.files[0];
        if (!file) return alert("⚠️ Please upload an image first.");

        elements.loadingIndicator.style.display = "block";
        outputElement.style.display = "none";
        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await fetch(url, { method: "POST", body: formData });
            const data = await response.json();

            if (data.error) {
                alert(`⚠️ Error: ${data.error}`);
                return;
            }

            if (data.prediction) {
                outputElement.innerText = prefix + data.prediction;
                outputElement.style.display = "block";
            } else if (data.gradcam) {
                outputElement.src = "data:image/jpeg;base64," + data.gradcam;
                outputElement.style.display = "block";
            } else {
                alert("⚠️ Error: No valid response received.");
            }
        } catch (error) {
            alert("⚠️ Error: Could not process image.");
        } finally {
            elements.loadingIndicator.style.display = "none";
        }
    }

    // 📩 Gửi request API chung
    async function fetchData(url, body = {}) {
        try {
            const response = await fetch(url, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(body)
            });
            return await response.json();
        } catch (error) {
            console.error(`❌ Fetch error: ${error}`);
            return { error: "Network error" };
        }
    }

    // 📩 Thêm tin nhắn vào hộp chat
    function addMessage(chatbox, text, className) {
        const messageDiv = document.createElement("div");
        messageDiv.className = className;
        messageDiv.textContent = text;
        chatbox.appendChild(messageDiv);
        chatbox.scrollTop = chatbox.scrollHeight;
    }
});
