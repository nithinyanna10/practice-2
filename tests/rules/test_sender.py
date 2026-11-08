from app.rules.sender import check_sender


def test_brand_claim_from_wrong_domain_flagged():
    r = check_sender("support@evil.io", "Microsoft Support")
    assert len(r) == 1 and r[0].startswith("sender_impersonation")


def test_brand_claim_from_real_domain_ok():
    assert check_sender("billing@microsoft.com", "Microsoft Billing") == []
    assert check_sender("x@mail.microsoft.com", "Microsoft") == []


def test_lookalike_domains_flagged():
    assert check_sender("a@microsoft.com.evil.io", "Microsoft")
    assert check_sender("a@notmicrosoft.com", "Microsoft")


def test_exec_title_from_freemail_flagged():
    assert check_sender("boss@gmail.com", "Jane Doe, CEO")


def test_exec_title_from_corporate_domain_ok():
    assert check_sender("jane@acme.com", "Jane Doe, CEO") == []


def test_angle_bracket_form_parsed():
    assert check_sender("Microsoft <support@evil.io>", "Microsoft")


def test_malformed_from_does_not_crash():
    assert check_sender("", "Microsoft")  # empty domain != brand, so flagged
    assert check_sender("nobody", "Alice") == []  # no claim, nothing to flag


def test_plain_name_no_claim_ok():
    assert check_sender("a@evil.io", "Alice Smith") == []


def test_one_reason_per_claim():
    r = check_sender("boss@gmail.com", "Microsoft CEO")
    assert len(r) == 2 and all(x.startswith("sender_impersonation") for x in r)


def test_brand_word_boundary_and_case():
    assert check_sender("a@evil.io", "Pineapple Co") == []  # "apple" inside a word
    assert check_sender("a@evil.io", "PAYPAL Support")
