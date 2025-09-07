<div align="center">

# 🤖 AI Hand Detection System

Real‑time hand detection and gesture insights with Python, OpenCV, and Flask — served via a sleek web UI.

[![Made with Python](https://img.shields.io/badge/Made%20with-Python-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-5C3EE8?logo=opencv&logoColor=white)](https://opencv.org/)
[![Flask](https://img.shields.io/badge/Flask-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

<br/>

🔗 Connect:<br/>
<a href="https://github.com/sunbyte16">
  <img alt="GitHub" src="https://img.shields.io/badge/GitHub-sunbyte16-181717?style=for-the-badge&logo=github&logoColor=white" />
</a>
<a href="https://www.linkedin.com/in/sunil-kumar-bb88bb31a/">
  <img alt="LinkedIn" src="https://img.shields.io/badge/LinkedIn-Sunil%20Sharma-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" />
</a>
<a href="https://lively-dodol-cc397c.netlify.app">
  <img alt="Portfolio" src="https://img.shields.io/badge/Portfolio-Visit-4CAF50?style=for-the-badge&logo=google-chrome&logoColor=white" />
</a>

<br/>

🧑‍💻 Created by <b>Sunil Sharma</b> ❤️

</div>

---

## ✨ Features

- **Real‑time detection**: Webcam stream processed on the backend, drawn as an overlay on the web UI
- **Multi‑hand support**: Detects up to two hands with bounding boxes, hulls, and centers
- **Gesture hinting**: Simple finger‑count estimation and on‑screen stats
- **Screenshots**: Save frames with timestamps via one click or hotkey
- **REST API**: Control start/stop and fetch frames/landmarks programmatically
- **Fast setup**: No heavyweight ML installs; works on Python 3.13 with OpenCV

## 🖥️ Demo

1) Start the server
```bash
python app.py
```
2) Open in your browser
```
http://localhost:5000
```

Tip: Grant the browser camera permission when prompted.

## 🚀 Quick Start

### Prerequisites
- Python 3.10+ (tested on 3.13)
- A webcam
- A modern browser (Chrome/Edge/Firefox)

### Install
```bash
pip install -r requirements.txt
```

### Run (Web UI)
```bash
python app.py
```
Then open `http://localhost:5000`.

### Optional: Desktop preview
```bash
python hand_detection.py
```

## 🎮 Controls (Web)
- Q: Quit (close tab)
- S: Save screenshot
- G: Toggle gesture mode

## 📡 API Endpoints

- `GET  /` — Web UI
- `POST /api/start` — Start detection pipeline
- `POST /api/stop` — Stop detection pipeline
- `GET  /api/status` — Running state and basic stats
- `GET  /api/frame` — Current frame as Base64 JPEG
- `GET  /api/landmarks` — Simplified contour landmarks
- `POST /api/screenshot` — Save current frame
- `GET  /health` — Health check

## 🧠 How It Works (High Level)

- The browser grants camera permission and displays the stream on a `<canvas>`.
- Flask starts a background capture thread with OpenCV (`cv2.VideoCapture`).
- Frames are processed with color‑space segmentation + contour analysis for a fast approximation of hands.
- The processed overlay is returned to the browser, which composites it with the live video.

## 🗂️ Project Structure

```
AI-hand-detection/
├── app.py                 # Flask API + background camera thread
├── hand_detection.py      # OpenCV-based detection utilities
├── templates/
│   └── index.html         # Web UI (canvas + controls)
├── requirements.txt       # Python dependencies
└── README.md              # You are here
```

## 🧩 Tech Stack

- Python, Flask
- OpenCV, NumPy
- HTML5 Canvas, Fetch API

## 🧪 Troubleshooting

- Black screen in browser:
  - Ensure the page has camera permission
  - Close other apps using the webcam
  - Refresh after clicking “Allow”
- No hands detected:
  - Improve lighting and avoid busy backgrounds
  - Keep the hand within the frame and at moderate distance
- Port already in use:
  - Change port in `app.py` or close the existing process

## 🤝 Contributing

Contributions are welcome! Please open an issue or a PR with a clear description.

## ⚖️ License

This project is available under the **MIT License**.

---

<div align="center">
Created by <b>❤️Sunil Sharma❤️</b> — keep building! ✋✨
</div>
