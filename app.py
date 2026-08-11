import os

from flask import Flask, render_template, request, redirect, session
from dotenv import load_dotenv
from neo4j import GraphDatabase
from queries import (
    get_all_jobs,
    get_job_details,
    get_skill_details,
    get_jobs_for_person,
    authenticate_person
)
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

URI = os.getenv("COGNODB_URI")
USERNAME = os.getenv("COGNODB_USERNAME")
PASSWORD = os.getenv("COGNODB_PASSWORD")

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        person = authenticate_person(email, password)

        if person:
            session["person_name"] = person["name"]
            session["person_email"] = person["email"]

            return redirect("/dashboard")

        return render_template(
            "login.html",
            error="Invalid email or password."
        )

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():

    if "person_name" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        person_name=session["person_name"],
        person_email=session["person_email"]
    )

@app.route("/")
def home():
    return redirect("/login")


@app.route("/health")
def health():
    try:
        driver.verify_connectivity()

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception:
        return {
            "status": "unhealthy",
            "database": "unreachable"
        }, 500

@app.route("/jobs")
def jobs():
    if "person_name" not in session:
            return redirect("/login")
    try:
        job_list = get_all_jobs()
        return render_template("jobs.html", jobs=job_list)

    except Exception:
        return render_template("error.html"), 500

@app.route("/jobs/<job_title>")
def job_details(job_title):
    if "person_name" not in session:
            return redirect("/login")
    try:
        job = get_job_details(job_title)

        if job is None:
            return "Job not found.", 404

        return render_template(
            "job_details.html",
            job=job
        )

    except Exception:
        return render_template("error.html"), 500

@app.route("/skills")
def skills():
    if "person_name" not in session:
            return redirect("/login")
    try:
        skill_list = [
            "Python",
            "SQL",
            "Flask",
            "FastAPI",
            "Django",
            "REST APIs",
            "Git",
            "Docker",
            "AWS",
            "Linux",
            "HTML",
            "CSS",
            "Java",
            "Spring Boot",
            "C++",
            "Machine Learning",
            "Pandas",
            "NumPy",
            "PostgreSQL",
            "MongoDB"
        ]

        return render_template(
            "skills.html",
            skills=skill_list
        )

    except Exception:
        return render_template("error.html"), 500

@app.route("/skills/<skill_name>")
def skill_details(skill_name):
    if "person_name" not in session:
            return redirect("/login")
    try:
        skill = get_skill_details(skill_name)

        if skill is None:
            return "Skill not found.", 404

        return render_template(
            "skill_details.html",
            skill=skill
        )

    except Exception:
        return render_template("error.html"), 500

@app.route("/matcher")
def matcher():

    if "person_name" not in session:
        return redirect("/login")

    try:
        person_name = session["person_name"]

        matches = get_jobs_for_person(person_name)

        return render_template(
            "matches.html",
            person_name=person_name,
            matches=matches
        )

    except Exception:
        return render_template("error.html"), 500

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

if __name__ == "__main__":
    app.run()