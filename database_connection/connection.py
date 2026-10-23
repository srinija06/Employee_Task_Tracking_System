
import mysql.connector
from mysql.connector import Error


def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Srinija@2501",
            database="employee_tracker"
        )

        if connection.is_connected():
            print("Successfully connected to MySQL!")
            return connection

    except Error as e:
        print("Error connecting to MySQL:", e)

    return None
