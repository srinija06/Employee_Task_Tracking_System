import mysql.connector

from database_connection.connection import create_connection
from utils.validators import is_valid_email


def get_all_employees():
    """Retrieve and display all employees."""

    connection = create_connection()

    if connection is None:
        print("Could not connect to the database.")
        return

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            SELECT employee_id, name, email, department,
                   job_title, employment_status
            FROM employees
            ORDER BY employee_id ASC
        """

        cursor.execute(query)
        employees = cursor.fetchall()

        if not employees:
            print("No employees found.")
            return

        print("\nEMPLOYEE LIST")
        print("-" * 100)

        for employee in employees:
            print(
                f"ID: {employee[0]} | "
                f"Name: {employee[1]} | "
                f"Email: {employee[2]} | "
                f"Department: {employee[3]} | "
                f"Job Title: {employee[4]} | "
                f"Status: {employee[5]}"
            )

        print("-" * 100)
        print(f"Total employees: {len(employees)}")

    except mysql.connector.Error as error:
        print(f"Database error: {error}")

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()

def add_employee():
    """Collect employee details and insert a new employee."""

    print("\nADD NEW EMPLOYEE")
    print("-" * 30)

    name = input("Enter employee name: ").strip()
    email = input("Enter employee email: ").strip()
    department = input("Enter department: ").strip()
    job_title = input("Enter job title: ").strip()

    # Validate required fields
    if not name or not email or not department or not job_title:
        print("Error: All fields are required.")
    return

    if not is_valid_email(email):
        print("Error: Please enter a valid email address.")
    return

    connection = create_connection()

    if connection is None:
        print("Could not connect to the database.")
        return

    cursor = None

    try:
        cursor = connection.cursor()

        query = """
            INSERT INTO employees
                (name, email, department, job_title)
            VALUES (%s, %s, %s, %s)
        """

        values = (name, email, department, job_title)

        cursor.execute(query, values)
        connection.commit()

        print(f"Employee '{name}' added successfully!")
        print(f"New employee ID: {cursor.lastrowid}")

    except mysql.connector.IntegrityError:
        connection.rollback()
        print("Error: This email address may already exist.")

    except mysql.connector.Error as error:
        connection.rollback()
        print(f"Database error: {error}")

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()
