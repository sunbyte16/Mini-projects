## 📰 Fake News Detector

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?logo=scikitlearn&logoColor=white)](https://scikit-learn.org/)
[![NLTK](https://img.shields.io/badge/NLTK-Text%20Processing-154F6D)](https://www.nltk.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-2E3440)](#)

Classify news headlines or articles as REAL or FAKE using TF‑IDF features with Logistic Regression and Naive Bayes. Clean preprocessing, strong baselines, and instant CLI prediction.

### ✨ Features
- 🔤 **Preprocessing**: lowercasing, punctuation removal, stopword removal, tokenization
- 🧮 **Vectorization**: TF‑IDF with unigrams + bigrams
- 🤖 **Models**: Logistic Regression, Multinomial Naive Bayes
- 📊 **Metrics**: accuracy, precision, recall, F1‑score
- 🧰 **CLI**: train/evaluate, predict custom text, save/load best model

### 📦 Requirements
Install once:
```
python -m pip install -r requirements.txt
```

### 📂 Dataset
Provide a CSV with at least:
- 📝 `text`: article body or headline
- 🏷️ `label`: `REAL` or `FAKE` (case‑insensitive; 1/0 supported)

A tiny sample is included at `data/news.csv` for a quick sanity check.

### 🚀 Quick Start
- 🏋️ Train & evaluate on the sample dataset and save the best model:
```
python fake_news_detector.py --data data/news.csv --save models/best_model.joblib
```
- ⚡ Predict without retraining (loads saved model):
```
python predict.py --model models/best_model.joblib --text "Government unveils economic plan"
```

### 🔧 Usage
- 🧪 Train & evaluate on your dataset:
```
python fake_news_detector.py --data path\to\your.csv
```
- 🗣️ Predict a custom text during training run (uses best model picked by F1):
```
python fake_news_detector.py --data path\to\your.csv --predict "Your headline here"
```
- 💾 Save best model + vectorizer for later use:
```
python fake_news_detector.py --data path\to\your.csv --save models\best_model.joblib
```

### 🗂️ Project Structure
```
Fake News Detector/
├─ 🧠 fake_news_detector.py   # train/eval + optional prediction and saving
├─ 🔍 predict.py              # load saved model for instant predictions
├─ 📦 requirements.txt
├─ 📁 data/
│  └─ 🧾 news.csv             # sample dataset
└─ 📁 models/
   └─ 📦 best_model.joblib    # created after --save (if run)
```

### 🛠️ Tech
- 🐍 Python
- 🧠 scikit‑learn
- 🧮 pandas, numpy
- 🔤 NLTK
- 💽 joblib

### 📬 Connect
[![GitHub](https://img.shields.io/badge/GitHub-sunbyte16-181717?logo=github)](https://github.com/sunbyte16)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Sunil%20Kumar-0A66C2?logo=linkedin&logoColor=white)](https://www.linkedin.com/in/sunil-kumar-bb88bb31a/)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit-4CAF50?logo=google-chrome&logoColor=white)](https://lively-dodol-cc397c.netlify.app)

---

 Created by **❤️Sunil Sharma❤️**
