from datetime import date
import mysql.connector
import pandas as pd

today_date = date.today()

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="9954",  # Replace with the actual password
    database="jobscout"  # Replace with the actual database name
)

class Login:
    @staticmethod
    def check_data(user, password):
        cursor = conn.cursor()
        # Query to fetch data for the given user and password
        query = "SELECT * FROM jobs_user WHERE user_id = %s AND password = %s"
        cursor.execute(query, (user, password))
        data = cursor.fetchall()

        if data:
            return 1
        else:
            return 0

class Signup:
    @staticmethod
    def create_data(name,user, password):
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobs_user (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_name VARCHAR(255),
                user_id VARCHAR(255) UNIQUE,
                password VARCHAR(255)
            );
        """)

        # Check if the user already exists
        query = "SELECT * FROM jobs_user WHERE user_id = %s"
        cursor.execute(query, (user,))
        data = cursor.fetchall()

        if data:
            # User already exists
            return 0
        else:
            # Insert new user data
            insert_query = "INSERT INTO jobs_user (user_name,user_id, password) VALUES (%s,%s, %s)"
            cursor.execute(insert_query, (name,user, password))
            conn.commit()
            return 0
