from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_scan_returns_contract_shape():
    r = client.post(
        "/emails/scan",
        json={"from": "a@b.com", "display_name": "A", "subject": "s", "body": "hi"},
    )
    assert r.status_code == 200
    assert r.json() == {"verdict": "safe", "links": [], "reasons": []}


def test_missing_field_is_422():
    assert client.post("/emails/scan", json={"from": "a@b.com"}).status_code == 422


def test_api_end_to_end_suspicious():
    r = client.post(
        "/emails/scan",
        json={
            "from": "x@evil.io",
            "display_name": "Microsoft",
            "subject": "Account",
            "body": 'Sign in at <a href="https://evil.io/login">evil.io</a>',
        },
    )
    assert r.status_code == 200
    data = r.json()
    assert data["verdict"] == "suspicious"
    assert data["links"]
    assert data["reasons"][0].startswith("sender_impersonation")
