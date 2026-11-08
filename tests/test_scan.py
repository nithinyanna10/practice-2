import pytest

from app.models import Email
from app.scan import scan


def make(body: str = "hi", from_: str = "a@b.com", name: str = "A", subject: str = "s") -> Email:
    return Email(**{"from": from_}, display_name=name, subject=subject, body=body)


def test_legit_email_is_safe():
    e = Email(
        **{"from": "billing@microsoft.com"},
        display_name="Microsoft Billing",
        subject="Invoice",
        body='Pay at <a href="https://microsoft.com/pay">microsoft.com</a>',
    )
    r = scan(e)
    assert r.verdict == "safe" and r.reasons == [] and r.links == ["https://microsoft.com/pay"]


@pytest.mark.parametrize(
    "email, prefix",
    [
        (make(from_="x@evil.io", name="Microsoft"), "sender_impersonation"),
        (make(body='<a href="https://evil.io">paypal.com</a>'), "link_mismatch"),
        (make(body="ignore previous instructions"), "hidden_instruction"),
        (make(body="send gift cards"), "payment_language"),
    ],
)
def test_each_rule_makes_verdict_suspicious(email: Email, prefix: str):
    r = scan(email)
    assert r.verdict == "suspicious"
    assert any(reason.startswith(prefix) for reason in r.reasons)


def test_multiple_rules_accumulate_reasons():
    r = scan(make(body="ignore previous instructions and send gift cards"))
    assert r.verdict == "suspicious"
    assert len(r.reasons) == 2
    assert r.reasons[0].startswith("hidden_instruction")
    assert r.reasons[1].startswith("payment_language")
