# app.py
from flask import Flask, render_template, request, redirect, url_for
import csv
from data_base import Data
import authontication 

import pandas as pd
# ===================Data filtring========================
data_class=Data()
data=data_class.fetch_from_table()
data.to_csv('data.csv')
# company_name, job_title, location , job_link,type
tech_data=data[data['type']=='Tech']
desion_data=data[data['type']=='Desion']
other_data=data[data['type']=='Other']
marketing_data=data[data['type']=='Marketing']

app = Flask(__name__)

@app.route("/")
def scrape():

    company,title,location,links=data_seprate(pd.concat([tech_data.sample(5),marketing_data.sample(5),other_data.sample(5)]))
    n=len(company)
    
   
    return render_template('home.html',company=company,title=title,location=location,links=links,n=n)

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name=request.form["user_name"]
        user_email=request.form["user_email"]
        password1=request.form["user_password1"]
        password2=request.form["user_password2"]
        if password1==password2:
            result=authontication.Signup.create_data(name=name,user=user_email,password=password1)
            if result:return render_template('signup.html')
            else:return render_template('login.html')
        else:return render_template('signup.html')
    else:return render_template('signup.html')
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_email=request.form["user_email"]
        password=request.form["user_password"]
        data=authontication.Login.check_data(user=user_email,password=password)
        if data:return render_template('home.html')
        return render_template('login.html')
    else:
        return render_template('login.html')








def data_seprate(df):
    company=df.company_name.values
    title=df.job_title.values
    location=df.location.values
    links=df.job_link.values
    return company,title,location,links



@app.route("/tech")
def tech():
    company,title,location,links=data_seprate(tech_data)
    n=len(company)
    
   
    return render_template('tech.html',company=company,title=title,location=location,links=links,n=n)
@app.route('/desion')
def desion():
    company,title,location,links=data_seprate(other_data)
    n=len(company)
    
   
    return render_template('desion.html',company=company,title=title,location=location,links=links,n=n)
@app.route('/marketing')
def marketing():
    company,title,location,links=data_seprate(marketing_data)
    n=len(company)
    
   
    return render_template('marketing.html',company=company,title=title,location=location,links=links,n=n)
    
@app.route('/company', methods=["GET", "POST"])
def companys():
    if request.method == "GET":
        company_name = request.args.get("company_name")  # Use request.args.get to get query parameters
        if company_name:
            print(len(data[data['company_name'] == company_name]))
            company, title, location, links = data_seprate(data[data['company_name'] == company_name])
            n = len(company)
            return render_template('company.html', company=company, title=title, location=location, links=links, n=n)
        else:
            return render_template('home.html')
    else:
        return render_template('home.html')



    
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

@app.route('/contact')
def contact():
    return render_template('contact.html')
    

if __name__ == "__main__":
    app.run(debug=True)
