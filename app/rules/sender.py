import re
from email.utils import parseaddr

from app.domains import domain_matches

BRANDS = {
    "microsoft": ["microsoft.com", "microsoftonline.com"],
    "google": ["google.com"],
    "paypal": ["paypal.com"],
    "amazon": ["amazon.com"],
    "apple": ["apple.com"],
}
EXEC_TITLES = ["ceo", "cfo", "cto", "coo", "president"]
FREE_MAIL = {"gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "aol.com", "proton.me"}


def _domain(from_addr: str) -> str:
    addr = parseaddr(from_addr)[1]
    return addr.rpartition("@")[2].lower() if "@" in addr else ""


def _has_word(word: str, text: str) -> bool:
    return re.search(rf"\b{re.escape(word)}\b", text, re.IGNORECASE) is not None


def check_sender(from_addr: str, display_name: str) -> list[str]:
    domain = _domain(from_addr)
    reasons = [
        f"sender_impersonation: display name claims {brand} but sender domain is {domain or 'missing'}"
        for brand, domains in BRANDS.items()
        if _has_word(brand, display_name) and not any(domain_matches(domain, d) for d in domains)
    ]
    if domain in FREE_MAIL or not domain:
        reasons += [
            f"sender_impersonation: display name claims {title.upper()} but sender uses {domain or 'no'} domain"
            for title in EXEC_TITLES
            if _has_word(title, display_name)
        ]
    return reasons
