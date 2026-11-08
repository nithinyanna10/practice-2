from fastapi import FastAPI

from app.models import Email, ScanResult
from app.scan import scan

app = FastAPI()


@app.post("/emails/scan", response_model=ScanResult)
def scan_email(email: Email) -> ScanResult:
    return scan(email)
