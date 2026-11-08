import time

from app.links import Anchor
from app.rules.link_mismatch import check_link_mismatch


def test_text_domain_differs_from_href_flagged():
    r = check_link_mismatch([Anchor("https://paypal.com.evil.io/login", "www.paypal.com")])
    assert len(r) == 1 and r[0].startswith("link_mismatch")


def test_matching_domains_ok():
    assert check_link_mismatch([Anchor("https://www.paypal.com/x", "paypal.com")]) == []
    assert check_link_mismatch([Anchor("https://bank.com/login", "https://bank.com")]) == []


def test_text_more_specific_than_href_ok():
    assert check_link_mismatch([Anchor("https://paypal.com/x", "www.paypal.com")]) == []


def test_text_without_domain_ok():
    assert check_link_mismatch([Anchor("https://evil.io", "Click here")]) == []
    assert check_link_mismatch([Anchor("https://evil.io", "")]) == []


def test_no_anchors_ok():
    assert check_link_mismatch([]) == []


def test_text_case_insensitive():
    assert check_link_mismatch([Anchor("https://bank.com/", "WWW.Bank.COM")]) == []


def test_domain_inside_sentence_uses_first_token():
    r = check_link_mismatch([Anchor("https://evil.io/", "Visit bank.com today")])
    assert len(r) == 1


def test_trailing_dot_host_ok():
    assert check_link_mismatch([Anchor("https://bank.com./x", "bank.com")]) == []


def test_one_reason_per_mismatching_anchor():
    anchors = [
        Anchor("https://evil.io/a", "bank.com"),
        Anchor("https://bank.com/b", "bank.com"),
        Anchor("https://evil.io/c", "shop.com"),
    ]
    r = check_link_mismatch(anchors)
    assert len(r) == 2 and all(x.startswith("link_mismatch") for x in r)


def test_bad_anchor_skipped_not_crashing():
    assert check_link_mismatch([Anchor("https://[bad/x", "bank.com"), Anchor("notaurl", "bank.com")]) == []


def test_perf_long_text_without_dot():
    start = time.perf_counter()
    assert check_link_mismatch([Anchor("https://evil.io", "a" * 200_000)]) == []
    assert time.perf_counter() - start < 1


def test_perf_long_dotted_text():
    start = time.perf_counter()
    assert check_link_mismatch([Anchor("https://evil.io", "a." * 100_000)]) == []
    assert time.perf_counter() - start < 1


def test_leading_dot_domain_still_flagged():
    assert check_link_mismatch([Anchor("https://evil.io", ".paypal.com")])
