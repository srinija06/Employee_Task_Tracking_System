
import mysql.connector

from database_connection.connection import create_connection


def assign_task(user):
    if not user or user.get("role") != "Admin":
        print("Access denied. Only Admin can assign tasks.")
        return
    """Assign a task to an active employee."""

    print("\nASSIGN TASK TO EMPLOYEE")
    print("-" * 30)

    # Step 1: Get task and employee IDs
    task_id = input("Enter Task ID: ").strip()
    employee_id = input("Enter Employee ID: ").strip()

    # Step 2: Validate IDs
    if not task_id.isdigit() or not employee_id.isdigit():
        print("Error: Task ID and Employee ID must be numbers.")
        return

    task_id = int(task_id)
    employee_id = int(employee_id)

    connection = create_connection()

    if connection is None:
        print("Could not connect to the database.")
        return

    cursor = None

    try:
        cursor = connection.cursor()

        # Step 3: Check whether the task exists
        cursor.execute(
            "SELECT task_id FROM tasks WHERE task_id = %s",
            (task_id,)
        )
        task = cursor.fetchone()

        if task is None:
            print("Error: Task not found.")
            return

        # Step 4: Check whether the employee exists and is active
        cursor.execute(
            """
            SELECT employee_id
            FROM employees
            WHERE employee_id = %s
              AND employment_status = 'Active'
            """,
            (employee_id,)
        )
        employee = cursor.fetchone()

        if employee is None:
            print("Error: Employee not found or is inactive.")
            return

        # Step 5: Insert the assignment
        cursor.execute(
            """
            INSERT INTO task_assignments (task_id, employee_id)
            VALUES (%s, %s)
            """,
            (task_id, employee_id)
        )

        connection.commit()

        print(
            f"Task {task_id} successfully assigned "
            f"to employee {employee_id}."
        )

    except mysql.connector.IntegrityError:
        connection.rollback()
        print("Error: This task may already be assigned to this employee.")

    except mysql.connector.Error as error:
        connection.rollback()
        print(f"Database error: {error}")

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()
