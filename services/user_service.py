
import getpass

import bcrypt
import mysql.connector

from database_connection.connection import create_connection


def create_employee_account(user):
    """Allow an administrator to create a login account for an employee."""

    if not user or user.get("role") != "Admin":
        print("Access denied. Only Admin can create employee accounts.")
        return
    print("\nCREATE EMPLOYEE LOGIN ACCOUNT")
    print("-" * 40)

    # Get the employee profile ID
    employee_id_input = input("Enter Employee ID: ").strip()

    if not employee_id_input.isdigit():
        print("Error: Employee ID must be a positive number.")
        return

    employee_id = int(employee_id_input)

    # Get login details
    username = input("Enter a username: ").strip()

    if not username:
        print("Error: Username cannot be empty.")
        return

    password = getpass.getpass("Enter temporary password: ")
    confirm_password = getpass.getpass("Confirm temporary password: ")

    if len(password) < 12:
        print("Error: Password must contain at least 12 characters.")
        return

    if len(password.encode("utf-8")) > 72:
        print("Error: Password must not exceed 72 bytes for bcrypt.")
        return

    if password != confirm_password:
        print("Error: Passwords do not match.")
        return

    connection = create_connection()

    if connection is None:
        print("Could not connect to the database.")
        return

    cursor = None

    try:
        cursor = connection.cursor()

        # Check that the employee exists and is active
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

        # Prevent an employee from having multiple login accounts
        cursor.execute(
            "SELECT user_id FROM users WHERE employee_id = %s",
            (employee_id,)
        )

        if cursor.fetchone() is not None:
            print("Error: This employee already has a login account.")
            return

        # Hash the password before storing it
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        # Create an Employee account, not an Admin account
        cursor.execute(
            """
            INSERT INTO users (
                employee_id,
                username,
                password_hash,
                role,
                account_status
            )
            VALUES (%s, %s, %s, 'Employee', 'Active')
            """,
            (employee_id, username, password_hash)
        )

        connection.commit()

        print("\nEmployee login account created successfully!")
        print(f"Employee ID: {employee_id}")
        print(f"Username: {username}")
        print("Role: Employee")
        print("Give the temporary password securely to the employee.")

    except mysql.connector.IntegrityError:
        connection.rollback()
        print("Error: This username or employee account already exists.")

    except mysql.connector.Error as error:
        connection.rollback()
        print(f"Database error: {error}")

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()
