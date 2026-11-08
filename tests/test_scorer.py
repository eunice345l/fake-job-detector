import pytest

from app.scorer import score_text

SCAM_MESSAGES = [
    "Congratulations! You are selected. Pay a registration fee of Rs 999 to confirm your seat. Contact us on WhatsApp.",
    "Work from home, earn Rs 5000 per day. No interview, guaranteed job. Message us on Telegram today only.",
    "Urgent hiring! Send your CV to hr.careers@gmail.com and pay a refundable deposit to receive your offer letter.",
    "100% placement. Instant joining. Training fee of Rs 2500 required. Limited seats, hurry.",
    "Data entry job, no experience needed. Pay a processing fee and contact us on WhatsApp to start earning.",
]

GENUINE_MESSAGES = [
    "We are hiring a Python developer intern. Apply through our careers page. The process has a coding round and an interview.",
    "Software Engineer at Acme Technologies, Bengaluru. Requirements: B.Tech in Computer Science, knowledge of Java and SQL. Email careers@acme.com.",
    "Backend developer needed. You will build REST APIs, write unit tests and work with the team. There is no application fee.",
    "Our company is hiring a data analyst. Interviews are held online. Please apply on our official website.",
    "Junior QA engineer role. You will test web applications and report bugs. We offer a stipend and a learning plan.",
]


@pytest.mark.parametrize("message", SCAM_MESSAGES)
def test_scam_messages_are_not_low_risk(message):
    result = score_text(message)
    assert result["level"] in ("medium", "high"), result


@pytest.mark.parametrize("message", GENUINE_MESSAGES)
def test_genuine_messages_are_not_high_risk(message):
    result = score_text(message)
    assert result["level"] != "high", result