
import mysql.connector

from database_connection.connection import create_connection


def view_overdue_tasks():
    """Display tasks that are overdue and not completed."""

    print("\nOVERDUE TASKS REPORT")
    print("-" * 100)

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
                task_id,
                title,
                priority,
                due_date,
                status
            FROM tasks
            WHERE due_date < CURDATE()
              AND status != 'Completed'
            ORDER BY due_date ASC
            """
        )

        tasks = cursor.fetchall()

        if not tasks:
            print("No overdue tasks found.")
            return

        print(
            f"{'ID':<6}"
            f"{'TITLE':<35}"
            f"{'PRIORITY':<13}"
            f"{'DUE DATE':<15}"
            f"{'STATUS':<20}"
        )
        print("-" * 100)

        for task in tasks:
            print(
                f"{task[0]:<6}"
                f"{task[1][:33]:<35}"
                f"{task[2]:<13}"
               f"{task[3]!s:<15}"
                f"{task[4]:<20}"
            )

        print("-" * 100)
        print(f"Total overdue tasks: {len(tasks)}")

    except mysql.connector.Error as error:
        print(f"Database error: {error}")

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()


def view_employee_task_report():
    """Display task counts and assignments for each employee."""

    print("\nEMPLOYEE TASK REPORT")
    print("-" * 100)

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
                e.employee_id,
                e.name,
                COUNT(ta.task_id) AS total_tasks,
                SUM(
                    CASE WHEN t.status = 'Completed'
                    THEN 1 ELSE 0 END
                ) AS completed_tasks,
                SUM(
                    CASE WHEN t.status = 'Pending'
                    THEN 1 ELSE 0 END
                ) AS pending_tasks,
                SUM(
                    CASE WHEN t.status = 'In Progress'
                    THEN 1 ELSE 0 END
                ) AS in_progress_tasks
            FROM employees e
            LEFT JOIN task_assignments ta
                ON e.employee_id = ta.employee_id
            LEFT JOIN tasks t
                ON ta.task_id = t.task_id
            GROUP BY e.employee_id, e.name
            ORDER BY e.employee_id
            """
        )

        employees = cursor.fetchall()

        print(
            f"{'ID':<6}"
            f"{'EMPLOYEE NAME':<25}"
            f"{'TOTAL':<10}"
            f"{'COMPLETED':<13}"
            f"{'PENDING':<11}"
            f"{'IN PROGRESS':<15}"
        )
        print("-" * 100)

        for employee in employees:
            print(
                f"{employee[0]:<6}"
                f"{employee[1][:23]:<25}"
                f"{employee[2]:<10}"
                f"{employee[3] or 0:<13}"
                f"{employee[4] or 0:<11}"
                f"{employee[5] or 0:<15}"
            )

        print("-" * 100)
        print(f"Total employees displayed: {len(employees)}")

    except mysql.connector.Error as error:
        print(f"Database error: {error}")

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()


def view_task_completion_summary():
    """Display the number of tasks in each status."""

    print("\nTASK COMPLETION SUMMARY")
    print("-" * 50)

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
                status,
                COUNT(*) AS total_tasks
            FROM tasks
            GROUP BY status
            ORDER BY status
            """
        )

        results = cursor.fetchall()

        if not results:
            print("No tasks found.")
            return

        total_tasks = sum(row[1] for row in results)

        print(f"{'STATUS':<25}{'TOTAL TASKS':<15}")
        print("-" * 50)

        for status, count in results:
            percentage = (
                count / total_tasks * 100
                if total_tasks else 0
            )

            print(
                f"{status:<25}"
                f"{count:<15}"
                f"{percentage:.1f}%"
            )

        print("-" * 50)
        print(f"Total tasks: {total_tasks}")

    except mysql.connector.Error as error:
        print(f"Database error: {error}")

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()
