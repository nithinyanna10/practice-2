from app.models import Email, ScanResult


def scan(email: Email) -> ScanResult:
    return ScanResult(verdict="safe", links=[], reasons=[])
