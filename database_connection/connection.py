
import os

import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error

load_dotenv()


def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        if connection.is_connected():
            print("Successfully connected to MySQL!")
            return connection

    except Error as error:
        print("Error connecting to MySQL:", error)

    return None
