from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

SCAM = "Pay a registration fee of Rs 500 to confirm your seat. Contact us on WhatsApp. Email hr.jobs@gmail.com"
GENUINE = "We are hiring a Python developer. Apply on our careers page. The process has a coding round and an interview."


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_home_page_loads():
    response = client.get("/")
    assert response.status_code == 200
    assert "Fake Job Detector" in response.text


def test_scam_message_is_high_risk():
    response = client.post("/check", json={"text": SCAM})
    assert response.status_code == 200
    assert response.json()["level"] == "high"


def test_genuine_message_is_not_high_risk():
    response = client.post("/check", json={"text": GENUINE})
    assert response.status_code == 200
    assert response.json()["level"] != "high"


def test_response_has_expected_fields():
    data = client.post("/check", json={"text": SCAM}).json()
    for field in ("score", "level", "reasons", "rule_score", "model_probability"):
        assert field in data
    assert 0 <= data["score"] <= 100


def test_empty_text_is_rejected():
    response = client.post("/check", json={"text": ""})
    assert response.status_code == 400


def test_whitespace_only_text_is_rejected():
    response = client.post("/check", json={"text": "   \n  "})
    assert response.status_code == 400


def test_missing_text_field_is_rejected():
    response = client.post("/check", json={})
    assert response.status_code == 422


def test_very_long_text_is_rejected():
    response = client.post("/check", json={"text": "a" * 20001})
    assert response.status_code == 422