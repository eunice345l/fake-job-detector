import pandas as pd
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

from app.rules import analyze_text
from app.scorer import MODEL_WEIGHT, RULES_WEIGHT, load_model

df = pd.read_csv("data/fake_job_postings.csv")
text_cols = ["title", "company_profile", "description", "requirements", "benefits"]
df["text"] = df[text_cols].fillna("").agg(" ".join, axis=1)

_, X_test, _, y_test = train_test_split(
    df["text"], df["fraudulent"], test_size=0.2, stratify=df["fraudulent"], random_state=42
)

model = load_model()
probabilities = model.predict_proba(X_test)[:, 1]
rule_scores = [analyze_text(t)["score"] for t in X_test]

rules_only = [1 if s >= 20 else 0 for s in rule_scores]
model_only = [1 if p >= 0.5 else 0 for p in probabilities]
combined = [
    1 if min(100, MODEL_WEIGHT * p * 100 + RULES_WEIGHT * r) >= 50 else 0
    for p, r in zip(probabilities, rule_scores)
]

print("Results for the fake class")
print(f"{'Method':<14}{'Precision':>10}{'Recall':>10}{'F1':>10}")
for name, preds in [("Rules only", rules_only), ("Model only", model_only), ("Combined", combined)]:
    p = precision_score(y_test, preds, zero_division=0)
    r = recall_score(y_test, preds, zero_division=0)
    f = f1_score(y_test, preds, zero_division=0)
    print(f"{name:<14}{p:>10.2f}{r:>10.2f}{f:>10.2f}")