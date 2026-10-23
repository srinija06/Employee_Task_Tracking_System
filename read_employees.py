
import mysql.connector

from database_connection.connection import create_connection


def read_employees():
    # Step 1: Connect to MySQL
    connection = create_connection()

    if connection is None:
        print("Could not connect to the database.")
        return

    cursor = None

    try:
        # Step 2: Create a cursor
        cursor = connection.cursor()

        # Step 3: Execute the SQL query
        query = """
            SELECT *
            FROM employees
            ORDER BY employee_id ASC
        """
        cursor.execute(query)

        # Step 4: Fetch all employee records
        employees = cursor.fetchall()

        # Step 5: Display the records
        print("\nEMPLOYEE RECORDS")
        print("-" * 80)

        if not employees:
            print("No employee records found.")
        else:
            for employee in employees:
                print(employee)

        print("-" * 80)
        print("Total employees:", len(employees))

    except mysql.connector.Error as error:
        print("Database error:", error)

    finally:
        if cursor is not None:
            cursor.close()

        connection.close()
        print("Database connection closed.")


# Run the function
if __name__ == "__main__":
    read_employees()
