from unittest.mock import MagicMock, patch

import mysql.connector

from services.employee_service import add_employee



@patch("services.employee_service.create_connection")
@patch("builtins.input")
def test_add_employee_success(mock_input, mock_connection):
    """Test adding an employee with valid details."""

    mock_input.side_effect = [
        "Test Employee",
        "test.employee@example.com",
        "IT",
        "Developer",
    ]

    mock_db = MagicMock()
    mock_cursor = MagicMock()

    mock_connection.return_value = mock_db
    mock_db.cursor.return_value = mock_cursor
    mock_cursor.lastrowid = 101

    add_employee()

    mock_cursor.execute.assert_called_once_with(
        """
            INSERT INTO employees
                (name, email, department, job_title)
            VALUES (%s, %s, %s, %s)
        """,
        (
            "Test Employee",
            "test.employee@example.com",
            "IT",
            "Developer",
        ),
    )

    mock_db.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_db.close.assert_called_once()


@patch("services.employee_service.create_connection")
@patch("builtins.input")
def test_add_employee_rejects_invalid_email(
    mock_input, mock_connection
):
    """Test that an invalid email is rejected."""

    mock_input.side_effect = [
        "Test Employee",
        "invalid-email",
        "IT",
        "Developer",
    ]

    add_employee()

    mock_connection.assert_not_called()


@patch("services.employee_service.create_connection")
@patch("builtins.input")
def test_add_employee_rejects_missing_name(
    mock_input, mock_connection
):
    """Test that a missing employee name is rejected."""

    mock_input.side_effect = [
        "",
        "test.employee@example.com",
        "IT",
        "Developer",
    ]

    add_employee()

    mock_connection.assert_not_called()

@patch("services.employee_service.create_connection")
@patch("builtins.input")
def test_add_employee_database_error(mock_input, mock_connection):
    """Test that database errors trigger rollback."""

    mock_input.side_effect = [
        "Test Employee",
        "test.employee@example.com",
        "IT",
        "Developer",
    ]

    mock_db = MagicMock()
    mock_cursor = MagicMock()

    mock_connection.return_value = mock_db
    mock_db.cursor.return_value = mock_cursor

    mock_cursor.execute.side_effect = mysql.connector.Error(
    "Simulated database error"
)

    add_employee()

    mock_db.rollback.assert_called_once()
    mock_db.close.assert_called_once()
    mock_cursor.close.assert_called_once()
