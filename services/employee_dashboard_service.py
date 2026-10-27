
import mysql.connector

from database_connection.connection import create_connection


def view_my_tasks(user):
    """Display tasks assigned to the logged-in employee."""

    if not user or user.get("role") != "Employee":
        print("Access denied. Employee login is required.")
        return

    employee_id = user.get("employee_id")

    connection = create_connection()

    if connection is None:
        print("Could not connect to the database.")
        return

    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                t.task_id,
                t.title,
                t.priority,
                t.due_date,
                t.status
            FROM task_assignments AS ta
            JOIN tasks AS t
                ON ta.task_id = t.task_id
            WHERE ta.employee_id = %s
            ORDER BY t.due_date ASC, t.task_id ASC
            """,
            (employee_id,)
        )

        tasks = cursor.fetchall()

        print("\n========== MY ASSIGNED TASKS ==========")

        if not tasks:
            print("No tasks are currently assigned to you.")
            return

        print(
            f"{'Task ID':<10}"
            f"{'Title':<30}"
            f"{'Priority':<12}"
            f"{'Due Date':<15}"
            f"{'Status':<15}"
        )
        print("-" * 82)

        for task in tasks:
            print(
                f"{task[0]:<10}"
                f"{task[1][:28]:<30}"
                f"{task[2]:<12}"
                f"{task[3]!s:<15}"
                f"{task[4]:<15}"
            )

        print(f"\nTotal assigned tasks: {len(tasks)}")

    except mysql.connector.Error as error:
        print(f"Database error: {error}")

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()

def update_my_task_status(user):
    """Allow an employee to update the status of their assigned tasks."""

    if not user or user.get("role") != "Employee":
        print("Access denied. Employee login is required.")
        return

    employee_id = user.get("employee_id")

    print("\n========== UPDATE MY TASK STATUS ==========")

    task_id_input = input("Enter Task ID: ").strip()

    if not task_id_input.isdigit():
        print("Error: Task ID must be a positive number.")
        return

    task_id = int(task_id_input)

    allowed_statuses = {
        "1": "Pending",
        "2": "In Progress",
        "3": "Completed",
        "4": "On Hold"
    }

    print("\nChoose new status:")
    print("1. Pending")
    print("2. In Progress")
    print("3. Completed")
    print("4. On Hold")

    choice = input("Enter your choice: ").strip()

    if choice not in allowed_statuses:
        print("Error: Invalid status choice.")
        return

    new_status = allowed_statuses[choice]

    connection = create_connection()

    if connection is None:
        print("Could not connect to the database.")
        return

    cursor = None

    try:
        cursor = connection.cursor()

        # Verify that this task is assigned to the logged-in employee.
        cursor.execute(
            """
            SELECT t.status
            FROM task_assignments AS ta
            JOIN tasks AS t ON ta.task_id = t.task_id
            WHERE ta.task_id = %s
              AND ta.employee_id = %s
            """,
            (task_id, employee_id)
        )

        task = cursor.fetchone()

        if task is None:
            print("Error: This task is not assigned to your account.")
            return

        old_status = task[0]

        if old_status == new_status:
            print(f"The task is already marked as {new_status}.")
            return

        # Update the task and record the change in its history.
        cursor.execute(
            """
            UPDATE tasks
            SET status = %s
            WHERE task_id = %s
            AND EXISTS (
                SELECT 1
                FROM task_assignments
                WHERE task_assignments.task_id = tasks.task_id
                    AND task_assignments.employee_id = %s
            )
            """,
            (new_status, task_id, employee_id)
        )

        cursor.execute(
            """
            INSERT INTO task_history (
                task_id,
                changed_by,
                old_status,
                new_status,
                change_note
            )
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                task_id,
                employee_id,
                old_status,
                new_status,
                "Status updated by assigned employee"
            )
        )

        connection.commit()

        print(f"Task {task_id} status updated to {new_status}.")

    except mysql.connector.Error as error:
        connection.rollback()
        print(f"Database error: {error}")

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()

def add_my_task_comment(user):
    """Allow an employee to comment only on their assigned tasks."""

    if not user or user.get("role") != "Employee":
        print("Access denied. Employee login is required.")
        return

    employee_id = user.get("employee_id")

    task_id_input = input("Enter Task ID: ").strip()

    if not task_id_input.isdigit():
        print("Error: Task ID must be a positive number.")
        return

    task_id = int(task_id_input)

    comment_text = input("Enter your comment: ").strip()

    if not comment_text:
        print("Error: Comment cannot be empty.")
        return

    connection = create_connection()

    if connection is None:
        print("Could not connect to the database.")
        return

    cursor = None

    try:
        cursor = connection.cursor()

        # Verify the task is assigned to this employee.
        cursor.execute(
            """
            SELECT t.task_id
            FROM task_assignments AS ta
            JOIN tasks AS t ON ta.task_id = t.task_id
            WHERE ta.task_id = %s
              AND ta.employee_id = %s
            """,
            (task_id, employee_id)
        )

        if cursor.fetchone() is None:
            print("Error: This task is not assigned to your account.")
            return

        cursor.execute(
            """
            INSERT INTO comments (
                task_id,
                employee_id,
                comment_text
            )
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

def view_my_task_comments(user):
    """Allow an employee to view comments on their assigned tasks."""

    if not user or user.get("role") != "Employee":
        print("Access denied. Employee login is required.")
        return

    employee_id = user.get("employee_id")

    task_id_input = input("Enter Task ID: ").strip()

    if not task_id_input.isdigit():
        print("Error: Task ID must be a positive number.")
        return

    task_id = int(task_id_input)

    connection = create_connection()

    if connection is None:
        print("Could not connect to the database.")
        return

    cursor = None

    try:
        cursor = connection.cursor()

        # Confirm that the task belongs to this employee's assignments.
        cursor.execute(
            """
            SELECT task_id
            FROM task_assignments
            WHERE task_id = %s
              AND employee_id = %s
            """,
            (task_id, employee_id)
        )

        if cursor.fetchone() is None:
            print("Error: This task is not assigned to your account.")
            return

        # Retrieve comments for the assigned task.
        cursor.execute(
            """
            SELECT
                e.name,
                c.comment_text,
                c.created_at
            FROM comments AS c
            JOIN employees AS e
                ON c.employee_id = e.employee_id
            WHERE c.task_id = %s
            ORDER BY c.created_at ASC
            """,
            (task_id,)
        )

        comments = cursor.fetchall()

        print(f"\n========== COMMENTS FOR TASK {task_id} ==========")

        if not comments:
            print("No comments found for this task.")
            return

        for name, comment_text, created_at in comments:
            print(f"\nEmployee: {name}")
            print(f"Comment: {comment_text}")
            print(f"Date: {created_at}")
            print("-" * 40)

    except mysql.connector.Error as error:
        print(f"Database error: {error}")

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()
