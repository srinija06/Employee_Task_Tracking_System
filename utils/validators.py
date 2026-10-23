import re


def is_valid_email(email):
    """Check whether an email address has a valid basic format."""

    pattern = r"^[\w.-]+@[\w.-]+\.[a-zA-Z]{2,}$"

    return re.match(pattern, email) is not None