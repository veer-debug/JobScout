# app.py
from flask import Flask, render_template, request, redirect, url_for
import csv
from scrab import WebScraper

app = Flask(__name__)

@app.route("/")
def scrape():
   
    return render_template("home.html")

@app.route("/tech")
def tech():
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
    jobs = [
        {"title": "Software Engineer", "company": "Google", "location": "Mountain View, CA", "type": "Full-time", "description": "As a Software Engineer at Google, you will work on cutting-edge technologies to solve impactful problems."},
        {"title": "Data Scientist", "company": "Microsoft", "location": "Seattle, WA", "type": "Remote, Full-time", "description": "Join the Microsoft Data Science team to analyze large datasets and build predictive models."},
        {"title": "Frontend Developer", "company": "Amazon", "location": "New York, NY", "type": "Full-time", "description": "Work on developing scalable web applications using modern frontend technologies at Amazon."},
        {"title": "DevOps Engineer", "company": "Netflix", "location": "Los Gatos, CA", "type": "Full-time", "description": "Join Netflix's team as a DevOps Engineer to optimize and automate cloud infrastructure."},
        {"title": "UX/UI Designer", "company": "Apple", "location": "Cupertino, CA", "type": "Full-time", "description": "Design intuitive and impactful user interfaces for Apple's innovative products."},
        {"title": "Cybersecurity Analyst", "company": "Cisco", "location": "San Jose, CA", "type": "Remote, Full-time", "description": "Be a part of Cisco’s security team, where you will detect and mitigate cybersecurity threats."}
        ]
    return render_template('desion.html',jobs=jobs)
    

if __name__ == "__main__":
    app.run(debug=True)
