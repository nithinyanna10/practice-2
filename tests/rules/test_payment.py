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
