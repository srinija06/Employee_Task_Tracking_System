
import getpass

import bcrypt
import mysql.connector

from database_connection.connection import create_connection


def create_admin():
    print("\nCREATE FIRST ADMIN ACCOUNT")
    print("-" * 35)

    username = input("Enter admin username: ").strip()

    if not username:
        print("Error: Username cannot be empty.")
        return

    password = getpass.getpass("Enter admin password: ")
    confirm_password = getpass.getpass("Confirm admin password: ")

    if len(password) < 12:
        print("Error: Password must contain at least 12 characters.")
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

        # Find the dedicated admin employee profile
        cursor.execute(
            """
            SELECT employee_id
            FROM employees
            WHERE email = %s
              AND employment_status = 'Active'
            """,
            ("admin@employee-tracker.local",)
        )

        employee = cursor.fetchone()

        if employee is None:
            print("Error: Admin employee profile not found.")
            return

        employee_id = employee[0]

        # Check whether an admin account already exists
        cursor.execute(
            "SELECT user_id FROM users WHERE role = 'Admin'"
        )

        if cursor.fetchone() is not None:
            print("An admin account already exists.")
            return

        # Hash the password securely
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt()
        ).decode("utf-8")

        # Create the admin login
        cursor.execute(
            """
            INSERT INTO users (
                employee_id,
                username,
                password_hash,
                role,
                account_status
            )
            VALUES (%s, %s, %s, 'Admin', 'Active')
            """,
            (employee_id, username, password_hash)
        )

        connection.commit()
        print("Admin account created successfully!")

    except mysql.connector.IntegrityError:
        connection.rollback()
        print("Error: Username or employee account already exists.")

    except mysql.connector.Error as error:
        connection.rollback()
        print(f"Database error: {error}")

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()


if __name__ == "__main__":
    create_admin()
