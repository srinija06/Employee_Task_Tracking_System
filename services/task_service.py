
import mysql.connector

from database_connection.connection import create_connection


def get_all_tasks():
    """Retrieve and display all tasks."""

    connection = create_connection()

    if connection is None:
        print("Could not connect to the database.")
        return

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            SELECT
                task_id,
                title,
                priority,
                due_date,
                status,
                created_by
            FROM tasks
            ORDER BY task_id ASC
        """

        cursor.execute(query)
        tasks = cursor.fetchall()

        print("\nTASK LIST")
        print("-" * 100)

        if not tasks:
            print("No tasks found.")
            return

        for task in tasks:
            print(
                f"ID: {task[0]} | "
                f"Title: {task[1]} | "
                f"Priority: {task[2]} | "
                f"Due Date: {task[3]} | "
                f"Status: {task[4]} | "
                f"Created By: {task[5]}"
            )

        print("-" * 100)
        print(f"Total tasks: {len(tasks)}")

    except mysql.connector.Error as error:
        print(f"Database error: {error}")

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()

def create_task():
    """Create a new task and save it in MySQL."""

    print("\nCREATE NEW TASK")
    print("-" * 30)

    title = input("Enter task title: ").strip()
    description = input("Enter task description: ").strip()
    priority = input("Enter priority (Low/Medium/High/Critical): ").strip().title()
    due_date = input("Enter due date (YYYY-MM-DD): ").strip()

    try:
        created_by = int(input("Enter creator employee ID: "))
    except ValueError:
        print("Error: Employee ID must be a number.")
        return

    if not title or not due_date:
        print("Error: Task title and due date are required.")
        return

    if priority not in ("Low", "Medium", "High", "Critical"):
        print("Error: Invalid priority.")
        return

    connection = create_connection()

    if connection is None:
        print("Could not connect to the database.")
        return

    cursor = None

    try:
        cursor = connection.cursor()

        # Verify that the creator exists
        cursor.execute(
            "SELECT employee_id FROM employees WHERE employee_id = %s",
            (created_by,)
        )

        if cursor.fetchone() is None:
            print("Error: Creator employee not found.")
            return

        query = """
            INSERT INTO tasks
                (title, description, priority, due_date, created_by)
            VALUES (%s, %s, %s, %s, %s)
        """

        values = (title, description, priority, due_date, created_by)

        cursor.execute(query, values)
        connection.commit()

        print("Task created successfully!")
        print(f"New task ID: {cursor.lastrowid}")

    except mysql.connector.Error as error:
        connection.rollback()
        print(f"Database error: {error}")

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()

def update_task_status():
    """Update a task's status and record the change in history."""

    print("\nUPDATE TASK STATUS")
    print("-" * 30)

    try:
        task_id = int(input("Enter task ID: "))
        changed_by = int(input("Enter your employee ID: "))
    except ValueError:
        print("Error: Task ID and employee ID must be numbers.")
        return

    allowed_statuses = [
        "Pending",
        "In Progress",
        "Completed",
        "On Hold"
    ]

    new_status = input(
        "Enter new status (Pending/In Progress/Completed/On Hold): "
    ).strip().title()

    if new_status not in allowed_statuses:
        print("Error: Invalid task status.")
        return

    connection = create_connection()

    if connection is None:
        print("Could not connect to the database.")
        return

    cursor = None

    try:
        cursor = connection.cursor()

        # Get the current task status
        cursor.execute(
            "SELECT status FROM tasks WHERE task_id = %s",
            (task_id,)
        )
        task = cursor.fetchone()

        if task is None:
            print("Error: Task not found.")
            return

        old_status = task[0]

        # Verify the employee making the change
        cursor.execute(
            """
            SELECT employee_id
            FROM employees
            WHERE employee_id = %s
              AND employment_status = 'Active'
            """,
            (changed_by,)
        )

        if cursor.fetchone() is None:
            print("Error: Active employee not found.")
            return

        if old_status == new_status:
            print("The task already has this status.")
            return

        # Update the task status
        cursor.execute(
            "UPDATE tasks SET status = %s WHERE task_id = %s",
            (new_status, task_id)
        )

        # Record the change in task history
        cursor.execute(
            """
            INSERT INTO task_history
                (task_id, changed_by, old_status, new_status, change_note)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (
                task_id,
                changed_by,
                old_status,
                new_status,
                "Task status updated"
            )
        )

        connection.commit()

        print(f"Task {task_id} status updated successfully!")
        print(f"Previous status: {old_status}")
        print(f"New status: {new_status}")

    except mysql.connector.Error as error:
        connection.rollback()
        print(f"Database error: {error}")

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()

def search_tasks():
    """Search tasks by status or priority."""

    print("\nSEARCH AND FILTER TASKS")
    print("-" * 30)
    print("Leave a field empty to skip that filter.")

    status = input(
        "Enter status (Pending/In Progress/Completed/On Hold): "
    ).strip()

    priority = input(
        "Enter priority (Low/Medium/High/Critical): "
    ).strip().title()

    allowed_statuses = ["Pending", "In Progress", "Completed", "On Hold"]
    allowed_priorities = ["Low", "Medium", "High", "Critical"]

    if status and status not in allowed_statuses:
        print("Error: Invalid task status.")
        return

    if priority and priority not in allowed_priorities:
        print("Error: Invalid priority.")
        return

    query = """
        SELECT task_id, title, priority, due_date, status, created_by
        FROM tasks
        WHERE 1 = 1
    """
    values = []

    if status:
        query += " AND status = %s"
        values.append(status)

    if priority:
        query += " AND priority = %s"
        values.append(priority)

    query += " ORDER BY due_date ASC"

    connection = create_connection()

    if connection is None:
        print("Could not connect to the database.")
        return

    cursor = None

    try:
        cursor = connection.cursor()
        cursor.execute(query, tuple(values))
        tasks = cursor.fetchall()

        print("\nSEARCH RESULTS")
        print("-" * 100)

        if not tasks:
            print("No matching tasks found.")
            return

        for task in tasks:
            print(
                f"ID: {task[0]} | Title: {task[1]} | "
                f"Priority: {task[2]} | Due: {task[3]} | "
                f"Status: {task[4]} | Created By: {task[5]}"
            )

        print("-" * 100)
        print(f"Matching tasks: {len(tasks)}")

    except mysql.connector.Error as error:
        print(f"Database error: {error}")

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()
