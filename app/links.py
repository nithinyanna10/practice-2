import re
from dataclasses import dataclass
from html.parser import HTMLParser
from urllib.parse import urlsplit

_URL_RE = re.compile(r"https?://[^\s<>\"']+", re.IGNORECASE)
_PARTS_RE = re.compile(r"^(https?)://([^/?#]*)([^#]*)", re.IGNORECASE)
_TRAILING = ".,;:!?)]}"
_PAIRS = {")": "(", "]": "[", "}": "{"}


@dataclass(frozen=True)
class Anchor:
    href: str
    text: str


def _normalize(url: str) -> str:
    # Input is already entity-unescaped: HTMLParser unescapes text and attribute values.
    m = _PARTS_RE.match(url)
    if not m:
        return url
    scheme, host, rest = m.groups()
    return f"{scheme.lower()}://{host.lower()}{rest}"


def _valid(url: str) -> bool:
    """True for http(s) URLs with a host that urlsplit(...).hostname accepts."""
    if not _PARTS_RE.match(url):
        return False
    try:
        return bool(urlsplit(url).hostname)
    except ValueError:
        return False


def _strip_trailing(url: str) -> str:
    # A closing bracket is kept when it balances an opener inside the URL, e.g. Foo_(bar).
    while url and url[-1] in _TRAILING:
        c = url[-1]
        if c in _PAIRS and url.count(_PAIRS[c]) >= url.count(c):
            break
        url = url[:-1]
    return url


def _href(raw: str | None) -> str | None:
    url = (raw or "").strip()
    return _normalize(url) if _valid(url) else None


class _LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.anchors: list[Anchor] = []
        self.links: list[str] = []  # document order: hrefs and plain-text URLs
        self._href: str | None = None
        self._text: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return
        self._flush()
        self._href = _href(dict(attrs).get("href"))
        self._text = []
        if self._href:
            self.links.append(self._href)

    def handle_data(self, data: str) -> None:
        self._text.append(data)
        for m in _URL_RE.findall(data):
            url = _strip_trailing(m)
            if _valid(url):
                self.links.append(_normalize(url))

    def handle_endtag(self, tag: str) -> None:
        if tag == "a":
            self._flush()

    def _flush(self) -> None:
        if self._href:
            self.anchors.append(Anchor(self._href, "".join(self._text).strip()))
        self._href = None

    def close(self) -> None:
        super().close()
        self._flush()


def _parse(body: str) -> _LinkParser:
    parser = _LinkParser()
    parser.feed(body)
    parser.close()
    return parser


def extract_anchors(body: str) -> list[Anchor]:
    return _parse(body).anchors


def extract_links(body: str) -> list[str]:
    return list(dict.fromkeys(_parse(body).links))
