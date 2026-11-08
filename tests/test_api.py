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
