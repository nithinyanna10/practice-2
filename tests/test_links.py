import time

from app.links import Anchor, extract_anchors, extract_links


def test_plain_text_url_normalized():
    assert extract_links("Go to HTTP://Example.COM/Path#frag now") == ["http://example.com/Path"]


def test_html_href_extracted_and_entities_unescaped():
    assert extract_links('<a href="https://a.com/x?a=1&amp;b=2">hi</a>') == ["https://a.com/x?a=1&b=2"]


def test_trailing_punctuation_stripped():
    assert extract_links("See https://a.com/x.") == ["https://a.com/x"]


def test_same_url_in_href_and_text_listed_once():
    assert extract_links('<a href="https://a.com/">https://a.com/</a>') == ["https://a.com/"]


def test_non_http_hrefs_ignored():
    html = '<a href="mailto:x@y.com">m</a><a href="javascript:void(0)">j</a><a href="/rel">r</a>'
    assert extract_links(html) == []


def test_extract_anchors_returns_text_and_href():
    assert extract_anchors('<a href="https://evil.io/x"> www.paypal.com </a>') == [
        Anchor("https://evil.io/x", "www.paypal.com")
    ]


def test_no_links_and_stray_angle_brackets_do_not_crash():
    assert extract_links("") == [] and extract_links("a < b > c") == []


def test_first_seen_order_and_path_case_kept():
    assert extract_links("http://b.com/A then http://a.com/ then http://b.com/A") == [
        "http://b.com/A",
        "http://a.com/",
    ]


def test_anchor_non_http_skipped():
    assert extract_anchors('<a href="/rel">r</a><a>no href</a>') == []


def test_href_ending_in_closing_paren_listed_once_untruncated():
    url = "https://en.wikipedia.org/wiki/Foo_(bar)"
    assert extract_links(f'<a href="{url}">{url}</a>') == [url]


def test_href_ending_in_period_listed_once():
    assert extract_links('<a href="https://a.com/x.">link</a>') == ["https://a.com/x."]


def test_href_with_quote_listed_once():
    assert extract_links('<a href="https://a.com/it\'s">link</a>') == ["https://a.com/it's"]


def test_nbsp_after_plain_text_url_does_not_glue():
    assert extract_links("<p>Visit https://a.com/x&nbsp;now</p>") == ["https://a.com/x"]


def test_entity_brackets_do_not_glue():
    assert extract_links("<p>https://a.com/x&lt;b&gt;</p>") == ["https://a.com/x"]


def test_invalid_hosts_dropped_without_raising():
    body = '<a href="http://[">x</a><a href="https://">y</a> and https:// and http://['
    assert extract_links(body) == []
    assert extract_anchors(body) == []


def test_trailing_bracket_balance_preserved():
    assert extract_links("https://a.com/Foo_(bar).") == ["https://a.com/Foo_(bar)"]
    assert extract_links("(see https://a.com/x).") == ["https://a.com/x"]
    assert extract_links("https://a.com/x]") == ["https://a.com/x"]
    assert extract_links("https://a.com/x}.") == ["https://a.com/x"]


def test_perf_many_trailing_closers():
    start = time.perf_counter()
    assert extract_links("see https://a.com/x" + ")" * 150_000 + " ok") == ["https://a.com/x"]
    assert time.perf_counter() - start < 1
