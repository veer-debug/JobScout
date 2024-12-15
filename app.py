from flask import Flask, render_template, request, redirect, url_for
import csv
from data_base import Data
import authontication 
import pandas as pd
import os

# ===================Data filtering========================
data_class = Data()
data = data_class.fetch_from_table()
data.to_csv('data.csv')

# company_name, job_title, location, job_link, type
tech_data = data[data['type'] == 'Tech']
desion_data = data[data['type'] == 'Desion']
other_data = data[data['type'] == 'Other']
marketing_data = data[data['type'] == 'Marketing']

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
login_user_ = False
profile_data = None  # Default to None if no user is logged in

@app.route("/")
def scrape():
    company, title, location, links = data_separate(pd.concat([tech_data.sample(5), marketing_data.sample(5), other_data.sample(5)]))
    n = len(company)
    return render_template('home.html', company=company, title=title, location=location, links=links, n=n, login_user_=login_user_)

@app.route('/submit_application', methods=["POST"])
def submit_application():
    if request.method == "POST":
        user_name = request.form["user_name"]
        user_email = request.form["user_email"]
        college_name = request.form["college_name"]
        resume = request.files["resume"]

        if resume:
            resume_path = os.path.join(app.config['UPLOAD_FOLDER'], resume.filename)
            resume.save(resume_path)

            # Save application data to CSV
            with open('applications.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([user_name, user_email, college_name, resume.filename])

            return render_template('profile.html')
        else:
            return "Failed to submit application. Please try again."

@app.route('/signup', methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["user_name"]
        user_email = request.form["user_email"]
        password1 = request.form["user_password1"]
        password2 = request.form["user_password2"]
        if password1 == password2:
            result = authontication.Signup.create_data(name=name, user=user_email, password=password1)
            if result:
                return render_template('signup.html')
            else:
                return render_template('login.html')
        else:
            return render_template('signup.html')
    else:
        return render_template('signup.html')

def profile_extract(email):
    global profile_data
    profile_data = authontication.Login.fetch_user_profile(email)
    if profile_data:
        return profile_data
    else:
        return None

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_email = request.form["user_email"]
        password = request.form["user_password"]
        data = authontication.Login.check_data(user=user_email, password=password)
        if data:
            global login_user_
            login_user_ = True
            profile_extract(user_email)
            profile_name = profile_data['user_name'] if profile_data else None  # Ensure profile data exists
            return render_template('home.html', login_user_=login_user_, profile_name=profile_name)
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')

def data_separate(df):
    company = df.company_name.values
    title = df.job_title.values
    location = df.location.values
    links = df.job_link.values
    return company, title, location, links

@app.route("/tech")
def tech():
    company, title, location, links = data_separate(tech_data)
    n = len(company)
    profile_name = profile_data['user_name'] if profile_data else None  # Ensure profile data exists
    return render_template('tech.html', company=company, title=title, location=location, links=links, n=n, login_user_=login_user_, profile_name=profile_name)

@app.route('/desion')
def desion():
    company, title, location, links = data_separate(desion_data)
    n = len(company)
    profile_name = profile_data['user_name'] if profile_data else None  # Ensure profile data exists
    return render_template('desion.html', company=company, title=title, location=location, links=links, n=n, login_user_=login_user_, profile_name=profile_name)

@app.route('/marketing')
def marketing():
    company, title, location, links = data_separate(marketing_data)
    n = len(company)
    profile_name = profile_data['user_name'] if profile_data else None  # Ensure profile data exists
    return render_template('marketing.html', company=company, title=title, location=location, links=links, n=n, login_user_=login_user_, profile_name=profile_name)

@app.route('/company', methods=["GET", "POST"])
def companys():
    if request.method == "GET":
        company_name = request.args.get("company_name")  # Use request.args.get to get query parameters
        if company_name:
            company_data = data[data['company_name'] == company_name]
            company, title, location, links = data_separate(company_data)
            n = len(company)
            profile_name = profile_data['user_name'] if profile_data else None  # Ensure profile data exists
            return render_template('company.html', company=company, title=title, location=location, links=links, n=n, login_user_=login_user_, profile_name=profile_name)
        else:
            return render_template('home.html', login_user_=login_user_)
    else:
        return render_template('home.html', login_user_=login_user_)

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
    profile_name = profile_data['user_name'] if profile_data else None  # Ensure profile data exists
    return render_template('batch_2024.html', jobs=jobs, login_user_=login_user_, profile_name=profile_name)

@app.route('/contact')
def contact():
    profile_name = profile_data['user_name'] if profile_data else None  # Ensure profile data exists
    return render_template('contact.html', login_user_=login_user_, profile_name=profile_name)

@app.route("/profile")
def profile():
    if profile_data:
        user_id = profile_data['id']
        user_name = profile_data['user_name']
        user_email = profile_data['user_id']
        user_password = profile_data['password']
        user_date = profile_data['date_of_joining']
        key_words = authontication.Signup.fetch_skills(user_id=user_email)
        return render_template('profile.html', login_user_=login_user_, user_id=user_id, user_email=user_email, user_name=user_name, user_password=user_password, user_date=user_date, key_words=key_words)
    else:
        return render_template('login.html')  # Redirect to login if no profile data

@app.route("/add-interest")
def user_info():
    return render_template('user_info.html', login_user_=login_user_)

@app.route("/about")
def about_section():
    profile_name = profile_data['user_name'] if profile_data else None  # Ensure profile data exists
    return render_template('about.html', login_user_=login_user_, profile_name=profile_name)

if __name__ == '__main__':
    app.run(debug=True)
