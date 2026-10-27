from utils.validators import is_valid_email


def test_valid_email():
    assert is_valid_email("user@gmail.com") is True


def test_valid_email_with_subdomain():
    assert is_valid_email("test.employee@company.com") is True


def test_invalid_email_without_domain():
    assert is_valid_email("test@") is False


def test_invalid_email_format():
    assert is_valid_email("invalid-email") is False