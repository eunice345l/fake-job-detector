import re

FREE_EMAIL_DOMAINS = {
    "gmail.com", "yahoo.com", "outlook.com",
    "hotmail.com", "rediffmail.com",
}

MONEY_PHRASES = [
    "registration fee", "security deposit", "processing fee",
    "training fee", "application fee", "refundable deposit",
    "pay a fee", "kit charges",
]

URGENCY_PHRASES = [
    "apply immediately", "limited seats", "urgent", "hurry",
    "offer expires", "today only", "last chance",
]

TOO_GOOD_PHRASES = [
    "no interview", "guaranteed job", "100% placement",
    "no experience needed", "instant joining",
]

EARNINGS_PATTERN = re.compile(
    r"earn\s+(up to\s+)?(rs\.?|inr|₹)?\s*[\d,]{4,}\s*(per|/|a)\s*(day|week)"
)


def check_asks_for_money(text):
    for phrase in MONEY_PHRASES:
        position = text.find(phrase)
        if position == -1:
            continue
        before = text[max(0, position - 12):position]
        if "no " in before or "without " in before:
            continue
        return 40, f"Asks for money ('{phrase}')"
    return 0, None



def check_free_email(text):
    for domain in re.findall(r"[\w.\-]+@([\w.\-]+\.\w+)", text):
        if domain in FREE_EMAIL_DOMAINS:
            return 20, f"Uses a free email address ({domain}) instead of a company domain"
    return 0, None


def check_messaging_only(text):
    for app in ("whatsapp", "telegram"):
        if app in text:
            return 20, f"Asks you to contact them on {app.capitalize()}"
    return 0, None


def check_urgency(text):
    for phrase in URGENCY_PHRASES:
        if phrase in text:
            return 10, f"Creates pressure to act fast ('{phrase}')"
    return 0, None


def check_too_good_to_be_true(text):
    for phrase in TOO_GOOD_PHRASES:
        if phrase in text:
            return 15, f"Makes an unrealistic promise ('{phrase}')"
    if EARNINGS_PATTERN.search(text):
        return 20, "Promises very high daily or weekly earnings"
    return 0, None


RULES = [
    check_asks_for_money,
    check_free_email,
    check_messaging_only,
    check_urgency,
    check_too_good_to_be_true,
]


def analyze_text(text):
    text = text.lower()
    score = 0
    reasons = []
    for rule in RULES:
        points, reason = rule(text)
        if points:
            score += points
            reasons.append(reason)
    score = min(score, 100)
    if score < 20:
        level = "low"
    elif score < 50:
        level = "medium"
    else:
        level = "high"
    return {"score": score, "level": level, "reasons": reasons}