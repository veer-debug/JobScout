# app.py
from flask import Flask, render_template, request, redirect, url_for
import csv
from data_base import Data
import pandas as pd
# ===================Data filtring========================
data_class=Data()
data=data_class.fetch_from_table()
# company_name, job_title, location , job_link,type
tech_data=data[data['type']=='tech']
desion_data=data[data['type']=='Desion']
marketing_data=data[data['type']=='marketing']

app = Flask(__name__)

@app.route("/")
def scrape():
   
    return render_template("home.html")


@app.route('/signup')
def signup():
    return render_template('signup.html')
@app.route('/login')
def login():
    return render_template('login.html')








def data_seprate(df):
    company=tech_data['company_name']
    title=tech_data['job_title']
    location=tech_data['location']
    links=tech_data['job_link']
    return company,title,location,links



@app.route("/tech")
def tech():
    company,title,location,links=data_seprate(tech_data)
    jobs = [
        {"title": "Software Engineer", "company": "Google", "location": "Mountain View, CA", "type": "Full-time", "description": "As a Software Engineer at Google, you will work on cutting-edge technologies to solve impactful problems."},
        {"title": "Data Scientist", "company": "Microsoft", "location": "Seattle, WA", "type": "Remote, Full-time", "description": "Join the Microsoft Data Science team to analyze large datasets and build predictive models."},
        {"title": "Frontend Developer", "company": "Amazon", "location": "New York, NY", "type": "Full-time", "description": "Work on developing scalable web applications using modern frontend technologies at Amazon."},
        {"title": "DevOps Engineer", "company": "Netflix", "location": "Los Gatos, CA", "type": "Full-time", "description": "Join Netflix's team as a DevOps Engineer to optimize and automate cloud infrastructure."},
        {"title": "UX/UI Designer", "company": "Apple", "location": "Cupertino, CA", "type": "Full-time", "description": "Design intuitive and impactful user interfaces for Apple's innovative products."},
        {"title": "Cybersecurity Analyst", "company": "Cisco", "location": "San Jose, CA", "type": "Remote, Full-time", "description": "Be a part of Cisco’s security team, where you will detect and mitigate cybersecurity threats."}
        ]
    jobs = [
        {"title": "Software Engineer", "company": "Google", "location": "Mountain View, CA", "type": "Full-time", "description": "As a Software Engineer at Google, you will work on cutting-edge technologies to solve impactful problems."},
        {"title": "Data Scientist", "company": "Microsoft", "location": "Seattle, WA", "type": "Remote, Full-time", "description": "Join the Microsoft Data Science team to analyze large datasets and build predictive models."},
        {"title": "Frontend Developer", "company": "Amazon", "location": "New York, NY", "type": "Full-time", "description": "Work on developing scalable web applications using modern frontend technologies at Amazon."},
        {"title": "DevOps Engineer", "company": "Netflix", "location": "Los Gatos, CA", "type": "Full-time", "description": "Join Netflix's team as a DevOps Engineer to optimize and automate cloud infrastructure."},
        {"title": "UX/UI Designer", "company": "Apple", "location": "Cupertino, CA", "type": "Full-time", "description": "Design intuitive and impactful user interfaces for Apple's innovative products."},
        {"title": "Cybersecurity Analyst", "company": "Cisco", "location": "San Jose, CA", "type": "Remote, Full-time", "description": "Be a part of Cisco’s security team, where you will detect and mitigate cybersecurity threats."}
        ]
    return render_template('tech.html',jobs=jobs)
@app.route('/desion')
def desion():
    company,title,location,links=data_seprate(desion_data)
    jobs = [
        {"title": "Software Engineer", "company": "Google", "location": "Mountain View, CA", "type": "Full-time", "description": "As a Software Engineer at Google, you will work on cutting-edge technologies to solve impactful problems."},
        {"title": "Data Scientist", "company": "Microsoft", "location": "Seattle, WA", "type": "Remote, Full-time", "description": "Join the Microsoft Data Science team to analyze large datasets and build predictive models."},
        {"title": "Frontend Developer", "company": "Amazon", "location": "New York, NY", "type": "Full-time", "description": "Work on developing scalable web applications using modern frontend technologies at Amazon."},
        {"title": "DevOps Engineer", "company": "Netflix", "location": "Los Gatos, CA", "type": "Full-time", "description": "Join Netflix's team as a DevOps Engineer to optimize and automate cloud infrastructure."},
        {"title": "UX/UI Designer", "company": "Apple", "location": "Cupertino, CA", "type": "Full-time", "description": "Design intuitive and impactful user interfaces for Apple's innovative products."},
        {"title": "Cybersecurity Analyst", "company": "Cisco", "location": "San Jose, CA", "type": "Remote, Full-time", "description": "Be a part of Cisco’s security team, where you will detect and mitigate cybersecurity threats."}
        ]
    return render_template('desion.html',jobs=jobs)
@app.route('/marketing')
def marketing():
    company,title,location,links=data_seprate(marketing_data)
    jobs = [
        {"title": "Software Engineer", "company": "Google", "location": "Mountain View, CA", "type": "Full-time", "description": "As a Software Engineer at Google, you will work on cutting-edge technologies to solve impactful problems."},
        {"title": "Data Scientist", "company": "Microsoft", "location": "Seattle, WA", "type": "Remote, Full-time", "description": "Join the Microsoft Data Science team to analyze large datasets and build predictive models."},
        {"title": "Frontend Developer", "company": "Amazon", "location": "New York, NY", "type": "Full-time", "description": "Work on developing scalable web applications using modern frontend technologies at Amazon."},
        {"title": "DevOps Engineer", "company": "Netflix", "location": "Los Gatos, CA", "type": "Full-time", "description": "Join Netflix's team as a DevOps Engineer to optimize and automate cloud infrastructure."},
        {"title": "UX/UI Designer", "company": "Apple", "location": "Cupertino, CA", "type": "Full-time", "description": "Design intuitive and impactful user interfaces for Apple's innovative products."},
        {"title": "Cybersecurity Analyst", "company": "Cisco", "location": "San Jose, CA", "type": "Remote, Full-time", "description": "Be a part of Cisco’s security team, where you will detect and mitigate cybersecurity threats."}
        ]
    return render_template('marketing.html',jobs=jobs)
    
@app.route('/batch_2024')
def batch_2024():
    jobs = [
        {"title": "Software Engineer", "company": "Google", "location": "Mountain View, CA", "type": "Full-time", "description": "As a Software Engineer at Google, you will work on cutting-edge technologies to solve impactful problems."},
        {"title": "Data Scientist", "company": "Microsoft", "location": "Seattle, WA", "type": "Remote, Full-time", "description": "Join the Microsoft Data Science team to analyze large datasets and build predictive models."},
        {"title": "Frontend Developer", "company": "Amazon", "location": "New York, NY", "type": "Full-time", "description": "Work on developing scalable web applications using modern frontend technologies at Amazon."},
        {"title": "DevOps Engineer", "company": "Netflix", "location": "Los Gatos, CA", "type": "Full-time", "description": "Join Netflix's team as a DevOps Engineer to optimize and automate cloud infrastructure."},
        {"title": "UX/UI Designer", "company": "Apple", "location": "Cupertino, CA", "type": "Full-time", "description": "Design intuitive and impactful user interfaces for Apple's innovative products."},
        {"title": "Cybersecurity Analyst", "company": "Cisco", "location": "San Jose, CA", "type": "Remote, Full-time", "description": "Be a part of Cisco’s security team, where you will detect and mitigate cybersecurity threats."}
        ]
    return render_template('batch_2024.html',jobs=jobs)
    

if __name__ == "__main__":
    app.run(debug=True)
