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
