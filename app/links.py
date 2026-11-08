import html
import re
from dataclasses import dataclass
from html.parser import HTMLParser

_URL_RE = re.compile(r"https?://[^\s<>\"']+", re.IGNORECASE)
_PARTS_RE = re.compile(r"^(https?)://([^/?#]*)([^#]*)", re.IGNORECASE)
_TRAILING = ".,;:!?)]}"


@dataclass(frozen=True)
class Anchor:
    href: str
    text: str


def _normalize(url: str) -> str:
    url = html.unescape(url)
    m = _PARTS_RE.match(url)
    if not m:
        return url
    scheme, host, rest = m.groups()
    return f"{scheme.lower()}://{host.lower()}{rest}"


def _is_http(url: str) -> bool:
    return _PARTS_RE.match(url.strip()) is not None


class _AnchorParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.anchors: list[Anchor] = []
        self._href: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        self._flush()
        href = dict(attrs).get("href") or ""
        self._href = href.strip() if _is_http(href) else None
        self._text = []

    def handle_data(self, data: str) -> None:
        self._text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a":
            self._flush()

    def _flush(self) -> None:
        if self._href is not None:
            self.anchors.append(Anchor(_normalize(self._href), "".join(self._text).strip()))
        self._href = None

    def close(self) -> None:
        super().close()
        self._flush()


def extract_anchors(body: str) -> list[Anchor]:
    parser = _AnchorParser()
    parser.feed(body)
    parser.close()
    return parser.anchors


def extract_links(body: str) -> list[str]:
    # Regex also sees href values inside tags; anchors cover any it missed.
    found = [_normalize(m).rstrip(_TRAILING) for m in _URL_RE.findall(body)]
    found += [a.href for a in extract_anchors(body)]
    return list(dict.fromkeys(found))
