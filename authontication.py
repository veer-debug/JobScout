from datetime import date, datetime
import mysql.connector
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.ERROR, filename='app.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')

today_date = date.today()

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="9954",  
    database="jobscout"  
)

class Login:
    @staticmethod
    def check_data(user, password):
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM jobs_user WHERE user_id = %s AND password = %s"
            cursor.execute(query, (user, password))
            data = cursor.fetchall()

            if data:
                return 1
            else:
                return 0
        except mysql.connector.Error as e:
            logging.error(f"Error checking user data: {e}")
            return 0

    @staticmethod
    def fetch_user_profile(email_id):
        try:
            cursor = conn.cursor(dictionary=True)  # Use dictionary to get named columns
            query = "SELECT * FROM jobs_user WHERE user_id = %s"
            cursor.execute(query, (email_id,))
            profile_data = cursor.fetchone()  # Fetch only one result since user_id should be unique

            return profile_data
        except mysql.connector.Error as e:
            logging.error(f"Error fetching user profile: {e}")
            return None
class Signup:
    @staticmethod
    def create_data(name, user, password):
        try:
            date_of_joining = datetime.now().date()
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS jobs_user (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_name VARCHAR(255),
                    user_id VARCHAR(255) UNIQUE,
                    password VARCHAR(255),
                    date_of_joining DATE
                );
            """)

            query = "SELECT * FROM jobs_user WHERE user_id = %s"
            cursor.execute(query, (user,))
            data = cursor.fetchall()

            if data:
                return 0  # User already exists

            insert_query = "INSERT INTO jobs_user (user_name, user_id, password, date_of_joining) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (name, user, password, date_of_joining))
            conn.commit()
            return 1  # User successfully signed up
        except mysql.connector.Error as e:
            logging.error(f"Error creating user data: {e}")
            conn.rollback()  # Rollback in case of error
            return 0  # Failed to sign up

    @staticmethod
    def add_skills(user_id, skill):
        try:
            cursor = conn.cursor()

            # Create user_skills table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_skills (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id VARCHAR(255),
                    skill VARCHAR(255),
                    FOREIGN KEY (user_id) REFERENCES jobs_user(user_id)
                );
            """)

            # Update or insert skills for the given user
            # Check if the user exists
            cursor.execute("SELECT * FROM user_skills WHERE user_id = %s", (user_id,))
            data = cursor.fetchall()
            
            if data:
                
                # Update skills for the existing user
                cursor.execute("""
                    UPDATE user_skills 
                    SET skill = %s 
                    WHERE user_id = %s;
                """, (skill, user_id))
            else:
                
                # Insert new skill for the user if they do not exist
                cursor.execute("""
                    INSERT INTO user_skills (user_id, skill) 
                    VALUES (%s, %s);
                """, (user_id, skill))

            conn.commit()
            return 1  # Skills successfully added/updated
        except mysql.connector.Error as e:
            logging.error(f"Error adding/updating skills: {e}")
            conn.rollback()  # Rollback in case of error
            return 0  # Failed to add/update skills


    @staticmethod
    def fetch_skills(user_id):
        try:
            cursor = conn.cursor(dictionary=True)  # Use dictionary to get named columns
            query = "SELECT * FROM user_skills WHERE user_id = %s"
            cursor.execute(query, (user_id,))
            skills_data = cursor.fetchone()

            if skills_data:
                return  skills_data  # Return list of skills
            else:
                return None  # No skills found for the user
        except mysql.connector.Error as e:
            logging.error(f"Error fetching skills: {e}")
            return []  # Return an empty list in case of error

