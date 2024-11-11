from datetime import date
import mysql.connector
import pandas as pd

today_date = date.today()

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="9954",
    database="jobscout"
)

class Data:
    @staticmethod
    def add_to_table(dataframe):
        cursor = conn.cursor()
        
        # Check if the jobscout table exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobsdata (
                id INT AUTO_INCREMENT PRIMARY KEY,
                company_name VARCHAR(255),
                job_title VARCHAR(255),
                location VARCHAR(255)
                job_link VARCHAR(255),
                type VARCHAR(255)
            )
        """)  # Define columns based on your requirements

        # Prepare the insert query with the actual column names
        query = """INSERT INTO jobdata (company_name, job_title, location , job_link,type) VALUES (%s, %s, %s, %s, %s)"""
        
        # Insert each row from the 2D array
        for row in dataframe:
            cursor.execute(query, row)
        
        # Commit the transaction and close the cursor
        conn.commit()
        cursor.close()

    