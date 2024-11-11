from datetime import date
import mysql.connector
import pandas as pd

today_date = date.today()

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="9954",  # Replace 'your_password' with the actual password
    database="jobscout "    # Replace with the actual database name
)

class Data:
    @staticmethod
    def fetch_from_table():
        cursor = conn.cursor()
        # Check if the jobscout table exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS jobsdata (
                id INT AUTO_INCREMENT PRIMARY KEY,
                company_name VARCHAR(255),
                job_title VARCHAR(255),
                location VARCHAR(255),
                job_link VARCHAR(255),
                type VARCHAR(255)
            )
        """)  # Define columns based on your requirements
        
        # Query to fetch all columns for the given username
        query = """
            SELECT * 
            FROM jobsdata
        """
        
        cursor.execute(query)
        
        # Fetch all matching rows
        all_data = cursor.fetchall()
        
        # Get column names from the cursor description
        columns = [col[0] for col in cursor.description]
        
        # Convert to DataFrame
        df = pd.DataFrame(all_data, columns=columns)
        
        # Close the cursor
        cursor.close()
        
        return df
         