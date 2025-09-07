import argparse
import os
import sys
import joblib
import fake_news_detector  # Ensure module is imported
from fake_news_detector import clean_text  # Expose global name for unpickling


def main():
    parser = argparse.ArgumentParser(description="Predict REAL/FAKE for a given text using a saved model")
    parser.add_argument("--model", default="models/best_model.joblib", help="Path to saved joblib model")
    parser.add_argument("--text", default=None, help="Text to classify. If omitted, reads from stdin.")
    args = parser.parse_args()

    if not os.path.exists(args.model):
        print(f"Model not found at: {args.model}. Train and save one first.")
        sys.exit(1)

    bundle = joblib.load(args.model)
    model = bundle.get("model")
    vectorizer = bundle.get("vectorizer")

    if args.text is None:
        print("Enter text to classify (Ctrl+Z then Enter to end on Windows):")
        text = sys.stdin.read().strip()
    else:
        text = args.text

    if not text:
        print("No text provided.")
        sys.exit(1)

    X = vectorizer.transform([text])
    proba = None
    if hasattr(model, "predict_proba"):
        proba = float(model.predict_proba(X)[0][1])
    elif hasattr(model, "decision_function"):
        score = float(model.decision_function(X)[0])
        proba = 1.0 / (1.0 + (2.718281828459045 ** (-score)))
    else:
        proba = float(model.predict(X)[0])

    label = "REAL" if proba >= 0.5 else "FAKE"
    print(f"Result: {label} (confidence={proba:.4f})")


if __name__ == "__main__":
    main()
