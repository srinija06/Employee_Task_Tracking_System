
import mysql.connector

from database_connection.connection import create_connection


def add_comment():
    """Add a comment to a task."""

    print("\nADD TASK COMMENT")
    print("-" * 30)

    task_id = input("Enter Task ID: ").strip()
    employee_id = input("Enter Employee ID: ").strip()
    comment_text = input("Enter your comment: ").strip()

    # Validate input
    if not task_id.isdigit() or not employee_id.isdigit():
        print("Error: Task ID and Employee ID must be numbers.")
        return

    if not comment_text:
        print("Error: Comment cannot be empty.")
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

        # Check whether the task exists
        cursor.execute(
            "SELECT task_id FROM tasks WHERE task_id = %s",
            (task_id,)
        )
        task = cursor.fetchone()

        if task is None:
            print("Error: Task not found.")
            return

        # Check whether the employee exists and is active
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

        # Save the comment
        cursor.execute(
            """
            INSERT INTO comments (task_id, employee_id, comment_text)
            VALUES (%s, %s, %s)
            """,
            (task_id, employee_id, comment_text)
        )

        connection.commit()

        print("Comment added successfully!")

    except mysql.connector.Error as error:
        connection.rollback()
        print(f"Database error: {error}")

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()


def view_task_comments():
    """Display all comments for a selected task."""

    print("\nVIEW TASK COMMENTS")
    print("-" * 30)

    task_id = input("Enter Task ID: ").strip()

    if not task_id.isdigit():
        print("Error: Task ID must be a number.")
        return

    task_id = int(task_id)

    connection = create_connection()

    if connection is None:
        print("Could not connect to the database.")
        return

    cursor = None

    try:
        cursor = connection.cursor()

        # Check whether the task exists
        cursor.execute(
            "SELECT title FROM tasks WHERE task_id = %s",
            (task_id,)
        )
        task = cursor.fetchone()

        if task is None:
            print("Error: Task not found.")
            return

        # Retrieve comments for the task
        cursor.execute(
            """
            SELECT
                c.employee_id,
                e.name,
                c.comment_text
            FROM comments c
            JOIN employees e
                ON c.employee_id = e.employee_id
            WHERE c.task_id = %s
            ORDER BY c.comment_id
            """,
            (task_id,)
        )

        comments = cursor.fetchall()

        print(f"\nTask: {task[0]}")
        print("-" * 80)

        if not comments:
            print("No comments found for this task.")
            return

        print(f"{'EMPLOYEE ID':<15}{'EMPLOYEE NAME':<25}COMMENT")
        print("-" * 80)

        for comment in comments:
            print(
                f"{comment[0]:<15}"
                f"{comment[1]:<25}"
                f"{comment[2]}"
            )

        print("-" * 80)
        print(f"Total comments: {len(comments)}")

    except mysql.connector.Error as error:
        print(f"Database error: {error}")

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()
