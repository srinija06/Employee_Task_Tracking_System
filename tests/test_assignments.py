
from unittest.mock import patch

from services.assignment_service import assign_task


@patch("services.assignment_service.create_connection")
@patch("builtins.input")
def test_assign_task_denies_employee(mock_input, mock_connection):
    """Ensure an Employee cannot assign tasks."""

    assign_task({"role": "Employee"})

    mock_connection.assert_not_called()
    mock_input.assert_not_called()
