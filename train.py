import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.metrics import classification_report

df = pd.read_csv("data/fake_job_postings.csv")

text_cols = ["title", "company_profile", "description", "requirements", "benefits"]
df["text"] = df[text_cols].fillna("").agg(" ".join, axis=1)

X = df["text"]
y = df["fraudulent"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

model = make_pipeline(
    TfidfVectorizer(stop_words="english", max_features=20000, ngram_range=(1, 2)),
    LogisticRegression(max_iter=1000, class_weight="balanced"),
)

model.fit(X_train, y_train)

predictions = model.predict(X_test)
print(classification_report(y_test, predictions, target_names=["real", "fake"]))

joblib.dump(model, "model.joblib")
print("Model saved to model.joblib")