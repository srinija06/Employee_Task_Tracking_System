
from database_connection.connection import create_connection

connection = create_connection()

if connection is not None:
    print("Database connection test: SUCCESS!")
    connection.close()
    print("Database connection closed.")
else:
    print("Database connection test: FAILED!")
