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


def update_employee():
    """Update an existing employee's details."""

    print("\nUPDATE EMPLOYEE")
    print("-" * 30)

    try:
        employee_id = int(input("Enter employee ID to update: "))
    except ValueError:
        print("Error: Employee ID must be a number.")
        return

    connection = create_connection()

    if connection is None:
        print("Could not connect to the database.")
        return

    cursor = None

    try:
        cursor = connection.cursor()

        # Check whether the employee exists
        cursor.execute(
            "SELECT employee_id FROM employees WHERE employee_id = %s",
            (employee_id,)
        )

        if cursor.fetchone() is None:
            print("Error: Employee not found.")
            return

        name = input("Enter new name: ").strip()
        email = input("Enter new email: ").strip()
        department = input("Enter new department: ").strip()
        job_title = input("Enter new job title: ").strip()

        if not name or not email or not department or not job_title:
            print("Error: All fields are required.")
            return

        if not is_valid_email(email):
            print("Error: Please enter a valid email address.")
            return

        query = """
            UPDATE employees
            SET name = %s,
                email = %s,
                department = %s,
                job_title = %s
            WHERE employee_id = %s
        """

        values = (name, email, department, job_title, employee_id)

        cursor.execute(query, values)
        connection.commit()

        print("Employee updated successfully!")

    except mysql.connector.IntegrityError:
        connection.rollback()
        print("Error: That email address may already belong to another employee.")

    except mysql.connector.Error as error:
        connection.rollback()
        print(f"Database error: {error}")

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()


def deactivate_employee():
    """Mark an employee as inactive without deleting their history."""

    print("\nDEACTIVATE EMPLOYEE")
    print("-" * 30)

    try:
        employee_id = int(input("Enter employee ID to deactivate: "))
    except ValueError:
        print("Error: Employee ID must be a number.")
        return

    connection = create_connection()

    if connection is None:
        print("Could not connect to the database.")
        return

    cursor = None

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT employment_status
            FROM employees
            WHERE employee_id = %s
            """,
            (employee_id,)
        )

        employee = cursor.fetchone()

        if employee is None:
            print("Error: Employee not found.")
            return

        if employee[0] == "Inactive":
            print("This employee is already inactive.")
            return

        cursor.execute(
            """
            UPDATE employees
            SET employment_status = 'Inactive'
            WHERE employee_id = %s
            """,
            (employee_id,)
        )

        connection.commit()
        print(f"Employee ID {employee_id} deactivated successfully.")

    except mysql.connector.Error as error:
        connection.rollback()
        print(f"Database error: {error}")

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()


