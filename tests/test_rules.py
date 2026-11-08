from app.rules import analyze_text


def test_money_request_is_flagged():
    result = analyze_text("Pay a registration fee of Rs 500 to confirm your seat")
    assert result["score"] >= 40
    assert any("money" in r.lower() for r in result["reasons"])


def test_free_email_is_flagged():
    result = analyze_text("Send your CV to hr.jobs@gmail.com")
    assert result["score"] == 20


def test_company_email_is_not_flagged():
    result = analyze_text("Send your CV to careers@acme.com")
    assert result["score"] == 0


def test_whatsapp_only_is_flagged():
    result = analyze_text("Contact us only on WhatsApp")
    assert result["score"] == 20


def test_normal_post_is_low_risk():
    result = analyze_text(
        "We are hiring a Python intern. Apply through our careers page. "
        "The process includes a coding round and a short interview."
    )
    assert result["score"] == 0
    assert result["level"] == "low"


def test_several_warning_signs_give_high_risk():
    result = analyze_text(
        "Pay a registration fee. Contact us on WhatsApp. Email hr.jobs@gmail.com"
    )
    assert result["score"] == 80
    assert result["level"] == "high"


def test_score_never_goes_above_100():
    result = analyze_text(
        "Pay a registration fee. WhatsApp us at hr@gmail.com. "
        "Urgent! No interview, guaranteed job."
    )
    assert result["score"] == 100


def test_empty_text_is_safe():
    assert analyze_text("")["score"] == 0


def test_harmless_mention_of_fee_is_not_flagged():
    result = analyze_text("There is no application fee. Applying is completely free.")
    assert result["score"] == 0