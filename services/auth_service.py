
import getpass
import bcrypt
import mysql.connector

from database_connection.connection import create_connection


def login():
    """Authenticate a user and return their account details."""

    print("\nEMPLOYEE TASK TRACKING SYSTEM - LOGIN")
    print("-" * 40)

    username = input("Enter username: ").strip()

    if not username:
        print("Error: Username cannot be empty.")
        return None

    password = getpass.getpass("Enter password: ")

    if not password:
        print("Error: Password cannot be empty.")
        return None

    connection = create_connection()

    if connection is None:
        print("Could not connect to the database.")
        return None

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        # Find the account using its username
        cursor.execute(
            """
            SELECT
                user_id,
                employee_id,
                username,
                password_hash,
                role,
                account_status
            FROM users
            WHERE username = %s
            """,
            (username,)
        )

        user = cursor.fetchone()

        # Check whether the username exists
        if user is None:
            print("Invalid username or password.")
            return None

        # Check whether the account is active
        if user["account_status"] != "Active":
            print("Your account is inactive. Contact the administrator.")
            return None

        # Verify the entered password against the stored bcrypt hash
        stored_hash = user["password_hash"].encode("utf-8")

        if not bcrypt.checkpw(password.encode("utf-8"), stored_hash):
            print("Invalid username or password.")
            return None

        # Login successful: do not return the password hash
        logged_in_user = {
            "user_id": user["user_id"],
            "employee_id": user["employee_id"],
            "username": user["username"],
            "role": user["role"]
        }

        print(f"\nLogin successful! Welcome, {user['username']}.")
        print(f"Role: {user['role']}")

        return logged_in_user

    except mysql.connector.Error as error:
        print(f"Database error: {error}")
        return None

    except (ValueError, TypeError):
        print("Error: The stored password hash is invalid.")
        return None

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()


if __name__ == "__main__":
    login()
