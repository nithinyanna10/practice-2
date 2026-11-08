from app.links import extract_anchors, extract_links
from app.models import Email, ScanResult
from app.rules.injection import check_injection
from app.rules.link_mismatch import check_link_mismatch
from app.rules.payment import check_payment
from app.rules.sender import check_sender


def scan(email: Email) -> ScanResult:
    reasons = [
        *check_sender(email.from_, email.display_name),
        *check_link_mismatch(extract_anchors(email.body)),
        *check_injection(email.body),
        *check_payment(email.subject, email.body),
    ]
    return ScanResult(
        verdict="suspicious" if reasons else "safe",
        links=extract_links(email.body),
        reasons=reasons,
    )
