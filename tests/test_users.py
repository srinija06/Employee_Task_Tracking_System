
from unittest.mock import patch

from services.user_service import create_employee_account


@patch("services.user_service.create_connection")
@patch("builtins.input")
def test_create_employee_account_denies_employee(
    mock_input, mock_connection
):
    """Ensure an Employee cannot create employee accounts."""

    create_employee_account({"role": "Employee"})

    mock_connection.assert_not_called()
    mock_input.assert_not_called()


@patch("services.user_service.create_connection")
@patch("services.user_service.getpass.getpass")
@patch("builtins.input")
def test_create_account_rejects_short_password(
    mock_input, mock_getpass, mock_connection
):
    """Reject passwords shorter than 12 characters."""

    mock_input.side_effect = ["1", "testuser"]
    mock_getpass.side_effect = ["short123", "short123"]

    create_employee_account({"role": "Admin"})

    mock_connection.assert_not_called()


@patch("services.user_service.create_connection")
@patch("services.user_service.getpass.getpass")
@patch("builtins.input")
def test_create_account_rejects_mismatched_passwords(
    mock_input, mock_getpass, mock_connection
):
    """Reject passwords that do not match."""

    mock_input.side_effect = [
        "1",
        "testuser",
    ]
    mock_getpass.side_effect = [
        "SecurePassword123",
        "DifferentPassword123",
    ]

    create_employee_account({"role": "Admin"})

    mock_connection.assert_not_called()
