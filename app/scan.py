from app.links import extract_anchors, extract_links
from app.models import Email, ScanResult
from app.rules.injection import check_injection
from app.rules.link_mismatch import check_link_mismatch
from app.rules.payment import check_payment
from app.rules.sender import check_sender


MAX_BODY_CHARS = 1_000_000


def scan(email: Email) -> ScanResult:
    body = email.body[:MAX_BODY_CHARS]
    reasons = [
        *check_sender(email.from_, email.display_name),
        *check_link_mismatch(extract_anchors(body)),
        *check_injection(body),
        *check_payment(email.subject, body),
    ]
    if len(email.body) > MAX_BODY_CHARS:
        reasons.append("body_too_large")
    return ScanResult(
        verdict="suspicious" if reasons else "safe",
        links=extract_links(body),
        reasons=reasons,
    )
