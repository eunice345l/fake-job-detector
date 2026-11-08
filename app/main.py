from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from app.scorer import score_text

app = FastAPI(title="Fake Job Detector")

PAGE = Path(__file__).parent / "static" / "index.html"


class CheckRequest(BaseModel):
    text: str = Field(..., max_length=20000)


@app.get("/", response_class=HTMLResponse)
def home():
    return PAGE.read_text(encoding="utf-8")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/check")
def check(request: CheckRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Please paste some text to check.")
    return score_text(request.text)