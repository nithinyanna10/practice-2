from app.domains import domain_matches


def test_exact_and_subdomain_match():
    assert domain_matches("microsoft.com", "microsoft.com")
    assert domain_matches("Mail.Microsoft.com", "microsoft.com")


def test_lookalikes_do_not_match():
    assert not domain_matches("microsoft.com.evil.io", "microsoft.com")
    assert not domain_matches("notmicrosoft.com", "microsoft.com")
