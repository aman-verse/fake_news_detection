import sys
import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"

from pathlib import Path
from typing import Dict, Any
import joblib

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from nlp.preprocessing import clean_news_text, validate_input

MODEL_DIR = Path(__file__).resolve().parent
MODEL_PATH = MODEL_DIR / "fake_news_model.pkl"
VECTORIZER_PATH = MODEL_DIR / "tfidf_vectorizer.pkl"

_MODEL = None
_VECTORIZER = None

def load_model_and_vectorizer():
    global _MODEL, _VECTORIZER
    if _MODEL is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
        _MODEL = joblib.load(MODEL_PATH)
        
    if _VECTORIZER is None:
        if not VECTORIZER_PATH.exists():
            raise FileNotFoundError(f"Vectorizer file not found at {VECTORIZER_PATH}")
        _VECTORIZER = joblib.load(VECTORIZER_PATH)
        
    return _MODEL, _VECTORIZER

try:
    load_model_and_vectorizer()
except Exception:
    pass

def clean_text(text: str) -> str:
    return clean_news_text(text)

def predict_news_detailed(
    text: str,
    threshold: float = 0.50,
    uncertainty_margin: float = 0.12
) -> Dict[str, Any]:
    is_valid, error_msg = validate_input(text)
    if not is_valid:
        return {
            "prediction": "Uncertain",
            "verdict": "Uncertain",
            "confidence": 0.0,
            "probability_real": 0.50,
            "probability_fake": 0.50,
            "is_valid": False,
            "status": "invalid_input",
            "message": error_msg,
            "cleaned_text": "",
            "decision_basis": "input_guardrail"
        }
        
    cleaned = clean_news_text(text)
    if not cleaned:
        return {
            "prediction": "Uncertain",
            "verdict": "Uncertain",
            "confidence": 0.0,
            "probability_real": 0.50,
            "probability_fake": 0.50,
            "is_valid": False,
            "status": "empty_after_clean",
            "message": "Text contained no valid words after removing URLs and symbols.",
            "cleaned_text": "",
            "decision_basis": "input_guardrail"
        }
        
    model, vectorizer = load_model_and_vectorizer()
    vector = vectorizer.transform([cleaned])
    
    if vector.nnz == 0:
        return {
            "prediction": "Uncertain",
            "verdict": "Uncertain",
            "confidence": 0.0,
            "probability_real": 0.50,
            "probability_fake": 0.50,
            "is_valid": True,
            "status": "out_of_vocabulary",
            "message": "Input contains none of the learned vocabulary features.",
            "cleaned_text": cleaned,
            "decision_basis": "out_of_vocabulary"
        }
        
    if hasattr(model, "predict_proba"):
        probabilities = model.predict_proba(vector)[0]
        prob_fake = float(probabilities[0])
        prob_real = float(probabilities[1])
    else:
        decision = float(model.decision_function(vector)[0])
        import math
        prob_real = 1.0 / (1.0 + math.exp(-decision))
        prob_fake = 1.0 - prob_real
        
    lower_bound = threshold - uncertainty_margin
    upper_bound = threshold + uncertainty_margin
    
    if lower_bound <= prob_real <= upper_bound:
        prediction = "Uncertain"
        status = "uncertain"
        confidence = round(max(prob_real, prob_fake), 4)
        message = (
            f"The model is uncertain (P(Real)={prob_real*100:.1f}% is near the "
            f"{threshold*100:.0f}% threshold). Evidence verification is strongly recommended."
        )
    elif prob_real > threshold:
        prediction = "Real"
        status = "confident"
        confidence = round(prob_real, 4)
        message = f"Linguistic style aligns with authentic news reporting ({prob_real*100:.1f}% confidence)."
    else:
        prediction = "Fake"
        status = "confident"
        confidence = round(prob_fake, 4)
        message = f"Linguistic style aligns with misleading or sensational reporting ({prob_fake*100:.1f}% confidence)."
        
    return {
        "prediction": prediction,
        "verdict": prediction,
        "confidence": confidence,
        "probability_real": round(prob_real, 4),
        "probability_fake": round(prob_fake, 4),
        "is_valid": True,
        "status": status,
        "message": message,
        "cleaned_text": cleaned,
        "threshold": threshold,
        "decision_basis": "linguistic_classifier"
    }

def predict_news(text: str) -> str:
    result = predict_news_detailed(text, uncertainty_margin=0.0)
    pred = result.get("prediction", "Fake")
    if pred == "Uncertain":
        return "Real" if result.get("probability_real", 0.5) >= 0.5 else "Fake"
    return pred
