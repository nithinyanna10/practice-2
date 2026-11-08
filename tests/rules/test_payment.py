import time

import pytest

from app.rules.payment import check_payment


def test_wire_transfer_flagged():
    assert check_payment("", "Please send a Wire  Transfer today")


def test_gift_cards_flagged_in_subject():
    assert check_payment("Buy gift cards urgently", "")


def test_change_bank_details_flagged():
    assert check_payment("", "We need you to change bank details before Friday")
    assert check_payment("", "Update our banking account info")


def test_benign_ok():
    assert check_payment("Lunch", "See you at noon. Cards are on the table.") == []


def test_reason_prefix_and_distinct_phrases():
    reasons = check_payment("Wire transfer", "wire  TRANSFER now, plus gift card")
    assert len(reasons) == 2
    assert all(r.startswith("payment_language") for r in reasons)


def test_my_pronoun_flagged():
    for text in ("Please update my bank details", "change my banking account"):
        r = check_payment("", text)
        assert len(r) == 1 and r[0].startswith("payment_language")


@pytest.mark.parametrize("ws", [" ", "\n"])
def test_perf_whitespace_run_is_linear(ws):
    start = time.perf_counter()
    assert check_payment("", "update" + ws * 300_000) == []
    assert time.perf_counter() - start < 1
