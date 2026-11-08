import re
from urllib.parse import urlsplit

from app.domains import domain_matches
from app.links import Anchor

_DOMAIN_RE = re.compile(
    r"(?:https?://)?(?<![a-z0-9-])(?<![a-z0-9-]\.)((?:[a-z0-9-]+\.)+[a-z]{2,})"
)  # lookbehinds: start only at the head of a label run, so long runs are scanned once


def _host(href: str) -> str | None:
    try:
        host = urlsplit(href).hostname
    except ValueError:
        return None
    return host.rstrip(".") if host else None


def _mismatch(anchor: Anchor) -> str | None:
    m = _DOMAIN_RE.search(anchor.text.lower())
    host = _host(anchor.href) if m else None
    if not m or not host:
        return None
    text_domain = m.group(1)
    if domain_matches(host, text_domain) or domain_matches(text_domain, host):
        return None
    return f"link_mismatch: text shows {text_domain} but link goes to {host}"


def check_link_mismatch(anchors: list[Anchor]) -> list[str]:
    return [r for a in anchors if (r := _mismatch(a))]
