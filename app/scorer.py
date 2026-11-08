from pathlib import Path

import joblib

from app.rules import analyze_text

MODEL_PATH = Path(__file__).resolve().parent.parent / "model.joblib"
MODEL_WEIGHT = 0.6
RULES_WEIGHT = 0.8

_model = None


def load_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model


def level_from_score(score):
    if score < 20:
        return "low"
    if score < 50:
        return "medium"
    return "high"


def score_text(text):
    rules_result = analyze_text(text)
    probability = float(load_model().predict_proba([text])[0][1])
    model_score = probability * 100

    combined = min(
        100,
        round(MODEL_WEIGHT * model_score + RULES_WEIGHT * rules_result["score"]),
    )

    reasons = list(rules_result["reasons"])
    if probability >= 0.5:
        reasons.append(
            f"Text looks similar to known fake postings (model confidence {probability:.0%})"
        )

    return {
        "score": combined,
        "level": level_from_score(combined),
        "rule_score": rules_result["score"],
        "model_probability": round(probability, 3),
        "reasons": reasons,
    }