
from unittest.mock import MagicMock, patch

from services.assignment_service import assign_task
from services.task_service import create_task


@patch("services.task_service.create_connection")
@patch("builtins.input")
def test_create_task_success(mock_input, mock_connection):
    """Test creating a task with valid details."""

    mock_input.side_effect = [
        "Prepare Project Documentation",
        "Write project documentation",
        "High",
        "2026-11-15",
        "1",
    ]

    mock_db = MagicMock()
    mock_cursor = MagicMock()

    mock_connection.return_value = mock_db
    mock_db.cursor.return_value = mock_cursor

    # The creator employee exists.
    mock_cursor.fetchone.return_value = (1,)

    create_task({"role": "Admin"})

    mock_cursor.execute.assert_any_call(
        """
            INSERT INTO tasks
                (title, description, priority, due_date, created_by)
            VALUES (%s, %s, %s, %s, %s)
        """,
        (
            "Prepare Project Documentation",
            "Write project documentation",
            "High",
            "2026-11-15",
            1,
        ),
    )

    mock_db.commit.assert_called_once()
    mock_cursor.close.assert_called_once()
    mock_db.close.assert_called_once()

@patch("services.task_service.create_connection")
@patch("builtins.input")
def test_create_task_denies_employee(mock_input, mock_connection):
    """Ensure an Employee cannot create a task."""

    create_task({"role": "Employee"})

    mock_connection.assert_not_called()
    mock_input.assert_not_called()
@patch("services.assignment_service.create_connection")
@patch("builtins.input")
def test_assign_task_denies_employee(mock_input, mock_connection):
    """Ensure an Employee cannot assign tasks."""

    assign_task({"role": "Employee"})

    mock_connection.assert_not_called()
    mock_input.assert_not_called()