import re

_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("payment_language", re.compile(p, re.IGNORECASE))
    for p in (
        r"wire\s+transfer",
        r"gift\s+cards?",
        r"(change|update)\s+(of\s+)?(our|your|the)?\s*bank(ing)?\s+(details|account)",
    )
]


def check_payment(subject: str, body: str) -> list[str]:
    text = f"{subject}\n{body}"
    phrases: list[str] = []
    for label, regex in _PATTERNS:
        for m in regex.finditer(text):
            reason = f"{label}: {' '.join(m.group(0).lower().split())}"
            if reason not in phrases:
                phrases.append(reason)
    return phrases
