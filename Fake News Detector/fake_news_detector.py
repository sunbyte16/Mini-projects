import argparse
import os
import re
import sys
import warnings
from typing import Tuple

import joblib
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, precision_recall_fscore_support
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

import nltk
from nltk.corpus import stopwords

warnings.filterwarnings("ignore")

# Ensure NLTK stopwords are available
try:
    _ = stopwords.words("english")
except LookupError:
    nltk.download("stopwords")


def normalize_label(value):
    if isinstance(value, str):
        v = value.strip().lower()
        if v in {"real", "true", "reliable"}:
            return 1
        if v in {"fake", "false", "unreliable"}:
            return 0
    if isinstance(value, (int, float)):
        return 1 if int(value) == 1 else 0
    return np.nan


def clean_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    tokens = text.split()
    stops = set(stopwords.words("english"))
    tokens = [t for t in tokens if t not in stops]
    return " ".join(tokens)


def load_dataset(csv_path: str) -> Tuple[pd.Series, pd.Series]:
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset not found at: {csv_path}")
    df = pd.read_csv(csv_path)

    # Try common column names for text
    text_col_candidates = [
        "text",
        "content",
        "article",
        "headline",
        "title",
    ]
    label_col_candidates = ["label", "target", "y", "is_fake", "fake"]

    text_col = next((c for c in text_col_candidates if c in df.columns), None)
    label_col = next((c for c in label_col_candidates if c in df.columns), None)

    if text_col is None or label_col is None:
        raise ValueError(
            f"Expected columns not found. Got columns: {list(df.columns)}.\n"
            f"Text candidates: {text_col_candidates}\nLabel candidates: {label_col_candidates}"
        )

    X_raw = df[text_col].astype(str).fillna("")
    y_raw = df[label_col]
    y = y_raw.apply(normalize_label)

    valid_mask = y.notna() & X_raw.notna()
    X_raw = X_raw[valid_mask]
    y = y[valid_mask].astype(int)

    return X_raw.reset_index(drop=True), y.reset_index(drop=True)


def vectorize_text(train_texts: pd.Series, test_texts: pd.Series) -> Tuple[np.ndarray, np.ndarray, TfidfVectorizer]:
    vectorizer = TfidfVectorizer(
        preprocessor=clean_text,
        tokenizer=str.split,
        ngram_range=(1, 2),
        min_df=1,
        max_df=1.0,
        max_features=100000,
    )
    X_train = vectorizer.fit_transform(train_texts)
    X_test = vectorizer.transform(test_texts)
    return X_train, X_test, vectorizer


def train_models(X_train, y_train):
    models = {}

    lr = LogisticRegression(max_iter=200, n_jobs=None)
    models["LogisticRegression"] = lr.fit(X_train, y_train)

    nb = MultinomialNB()
    models["NaiveBayes"] = nb.fit(X_train, y_train)

    return models


def evaluate_models(models, X_test, y_test):
    results = {}
    for name, model in models.items():
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_test, y_pred, average="binary", zero_division=0
        )
        results[name] = {
            "accuracy": acc,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "report": classification_report(y_test, y_pred, target_names=["FAKE", "REAL"], zero_division=0),
        }
    return results


def pick_best_model(results, models):
    best_name = max(results, key=lambda k: results[k]["f1"])
    return best_name, models[best_name]


def predict_text(model, vectorizer, text: str) -> Tuple[str, float]:
    X = vectorizer.transform([text])
    proba = None
    if hasattr(model, "predict_proba"):
        proba = model.predict_proba(X)[0][1]
    elif hasattr(model, "decision_function"):
        # Map decision score to pseudo-probability via sigmoid
        score = model.decision_function(X)[0]
        proba = 1.0 / (1.0 + np.exp(-score))
    else:
        proba = float(model.predict(X)[0])
    label = "REAL" if proba >= 0.5 else "FAKE"
    return label, float(proba)


def main():
    parser = argparse.ArgumentParser(description="Fake News Detector")
    parser.add_argument("--data", required=True, help="Path to CSV dataset")
    parser.add_argument("--test_size", type=float, default=0.2, help="Test size fraction")
    parser.add_argument("--random_state", type=int, default=42, help="Random seed")
    parser.add_argument("--predict", type=str, default=None, help="Custom text to classify")
    parser.add_argument("--save", type=str, default=None, help="Path to save best model and vectorizer (joblib)")

    args = parser.parse_args()

    print("Loading dataset...")
    X_raw, y = load_dataset(args.data)

    print("Splitting train/test...")
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        X_raw, y, test_size=args.test_size, random_state=args.random_state, stratify=y
    )

    print("Vectorizing text (TF-IDF)...")
    X_train, X_test, vectorizer = vectorize_text(X_train_raw, X_test_raw)

    print("Training models...")
    models = train_models(X_train, y_train)

    print("Evaluating models...")
    results = evaluate_models(models, X_test, y_test)
    for name, metrics in results.items():
        print(f"\n=== {name} ===")
        print(f"Accuracy: {metrics['accuracy']:.4f}")
        print(f"Precision: {metrics['precision']:.4f}")
        print(f"Recall: {metrics['recall']:.4f}")
        print(f"F1-score: {metrics['f1']:.4f}")
        print(metrics["report"])

    best_name, best_model = pick_best_model(results, models)
    print(f"Best model: {best_name} (F1={results[best_name]['f1']:.4f})")

    if args.save:
        os.makedirs(os.path.dirname(args.save), exist_ok=True)
        joblib.dump({"model": best_model, "vectorizer": vectorizer}, args.save)
        print(f"Saved best model and vectorizer to: {args.save}")

    if args.predict is not None:
        label, proba = predict_text(best_model, vectorizer, args.predict)
        print(f"\nPrediction for input: {args.predict}")
        print(f"Result: {label} (confidence={proba:.4f})")


if __name__ == "__main__":
    main()
