import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

URI = os.getenv("COGNODB_URI")
USERNAME = os.getenv("COGNODB_USERNAME")
PASSWORD = os.getenv("COGNODB_PASSWORD")

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


skills = [
    ("Python", "Programming"),
    ("SQL", "Database"),
    ("Flask", "Backend"),
    ("FastAPI", "Backend"),
    ("Django", "Backend"),
    ("REST APIs", "Backend"),
    ("Git", "Tools"),
    ("Docker", "DevOps"),
    ("AWS", "Cloud"),
    ("Linux", "Operating System"),
    ("HTML", "Frontend"),
    ("CSS", "Frontend"),
    ("Java", "Programming"),
    ("Spring Boot", "Backend"),
    ("C++", "Programming"),
    ("Machine Learning", "AI/ML"),
    ("Pandas", "Data Science"),
    ("NumPy", "Data Science"),
    ("PostgreSQL", "Database"),
    ("MongoDB", "Database"),
]

companies = [
    ("TechNova", "Hyderabad"),
    ("CloudSphere", "Bangalore"),
    ("DataWorks", "Pune"),
    ("FinEdge", "Mumbai"),
    ("CodeCraft", "Chennai"),
    ("AI Solutions", "Hyderabad"),
]

jobs = [
    (
        "Python Developer",
        "Develop applications and backend services using Python.",
        "Entry Level",
        "TechNova"
    ),
    (
        "Backend Developer",
        "Build and maintain scalable backend services and APIs.",
        "Entry Level",
        "CloudSphere"
    ),
    (
        "Full Stack Developer",
        "Develop both frontend and backend components of web applications.",
        "Entry Level",
        "CodeCraft"
    ),
    (
        "Data Analyst",
        "Analyze data and create reports to support business decisions.",
        "Entry Level",
        "DataWorks"
    ),
    (
        "Data Engineer",
        "Build data pipelines and manage data processing systems.",
        "Entry Level",
        "DataWorks"
    ),
    (
        "ML Engineer",
        "Build and deploy machine learning models and applications.",
        "Entry Level",
        "AI Solutions"
    ),
    (
        "DevOps Engineer",
        "Automate deployment and manage cloud infrastructure.",
        "Entry Level",
        "CloudSphere"
    ),
    (
        "Java Developer",
        "Develop enterprise applications using Java and Spring Boot.",
        "Entry Level",
        "FinEdge"
    ),
    (
        "Software Engineer",
        "Design, develop, test and maintain software applications.",
        "Entry Level",
        "TechNova"
    ),
    (
        "Cloud Engineer",
        "Design and maintain cloud-based infrastructure and services.",
        "Entry Level",
        "AI Solutions"
    )
]

job_skills = {
    "Python Developer": [
        ("Python", "Required"),
        ("SQL", "Required"),
        ("Git", "Preferred"),
        ("REST APIs", "Preferred")
    ],

    "Backend Developer": [
        ("Python", "Required"),
        ("SQL", "Required"),
        ("REST APIs", "Required"),
        ("Flask", "Preferred"),
        ("Docker", "Preferred"),
        ("Git", "Preferred")
    ],

    "Full Stack Developer": [
        ("Python", "Required"),
        ("HTML", "Required"),
        ("CSS", "Required"),
        ("SQL", "Required"),
        ("REST APIs", "Preferred"),
        ("Git", "Preferred")
    ],

    "Data Analyst": [
        ("Python", "Required"),
        ("SQL", "Required"),
        ("Pandas", "Required"),
        ("NumPy", "Preferred")
    ],

    "Data Engineer": [
        ("Python", "Required"),
        ("SQL", "Required"),
        ("PostgreSQL", "Required"),
        ("Docker", "Preferred"),
        ("AWS", "Preferred"),
        ("Git", "Preferred")
    ],

    "ML Engineer": [
        ("Python", "Required"),
        ("Machine Learning", "Required"),
        ("NumPy", "Required"),
        ("Pandas", "Required"),
        ("Git", "Preferred"),
        ("Docker", "Preferred")
    ],

    "DevOps Engineer": [
        ("Linux", "Required"),
        ("Docker", "Required"),
        ("AWS", "Required"),
        ("Git", "Required"),
        ("Python", "Preferred")
    ],

    "Java Developer": [
        ("Java", "Required"),
        ("Spring Boot", "Required"),
        ("SQL", "Required"),
        ("Git", "Preferred"),
        ("Docker", "Preferred")
    ],

    "Software Engineer": [
        ("Python", "Preferred"),
        ("SQL", "Required"),
        ("Git", "Required"),
        ("Linux", "Preferred"),
        ("REST APIs", "Preferred")
    ],

    "Cloud Engineer": [
        ("AWS", "Required"),
        ("Linux", "Required"),
        ("Docker", "Required"),
        ("Git", "Preferred"),
        ("Python", "Preferred")
    ]
}

skill_relationships = [
    ("Python", "Flask"),
    ("Python", "FastAPI"),
    ("Python", "Django"),
    ("Python", "Pandas"),
    ("Python", "NumPy"),
    ("SQL", "PostgreSQL"),
    ("SQL", "MongoDB"),
    ("Docker", "AWS"),
    ("Docker", "Linux"),
    ("Machine Learning", "Python"),
    ("Machine Learning", "NumPy"),
    ("Machine Learning", "Pandas"),
    ("Java", "Spring Boot"),
    ("HTML", "CSS"),
    ("REST APIs", "Flask"),
    ("REST APIs", "FastAPI"),
]

persons = [
    ("Arjun", "arjun@example.com", "arjun123"),
    ("Priya", "priya@example.com", "priya123"),
    ("Rahul", "rahul@example.com", "rahul123"),
    ("Ananya", "ananya@example.com", "ananya123"),
    ("Vikram", "vikram@example.com", "vikram123"),
]

person_skills = {
    "Arjun": [
        ("Python", "Intermediate"),
        ("SQL", "Intermediate"),
        ("Flask", "Intermediate"),
        ("Git", "Intermediate"),
    ],

    "Priya": [
        ("Python", "Advanced"),
        ("SQL", "Advanced"),
        ("Pandas", "Intermediate"),
        ("NumPy", "Intermediate"),
        ("Machine Learning", "Intermediate"),
    ],

    "Rahul": [
        ("Java", "Intermediate"),
        ("Spring Boot", "Intermediate"),
        ("SQL", "Intermediate"),
        ("Git", "Intermediate"),
    ],

    "Ananya": [
        ("HTML", "Advanced"),
        ("CSS", "Advanced"),
        ("Python", "Intermediate"),
        ("REST APIs", "Intermediate"),
        ("SQL", "Beginner"),
    ],

    "Vikram": [
        ("Linux", "Intermediate"),
        ("Docker", "Intermediate"),
        ("AWS", "Intermediate"),
        ("Git", "Advanced"),
    ],
}

def seed_skills():
    with driver.session() as session:
        for name, category in skills:
            session.run(
                """
                MERGE (s:Skill {name: $name})
                SET s.category = $category
                """,
                name=name,
                category=category
            )

def seed_companies():
    with driver.session() as session:
        for name, location in companies:
            session.run(
                """
                MERGE (c:Company {name: $name})
                SET c.location = $location
                """,
                name=name,
                location=location
            )

def seed_jobs():
    with driver.session() as session:
        for title, description, experience_level, _ in jobs:
            session.run(
                """
                MERGE (j:Job {title: $title})
                SET j.description = $description
                SET j.experience_level = $experience_level
                """,
                title=title,
                description=description,
                experience_level=experience_level
            )

def seed_job_skills():
    with driver.session() as session:
        for job_title, required_skills in job_skills.items():
            for skill_name, importance in required_skills:
                session.run(
                    """
                    MATCH (j:Job {title: $job_title})
                    MATCH (s:Skill {name: $skill_name})
                    MERGE (j)-[:REQUIRES {importance: $importance}]->(s)
                    """,
                    job_title=job_title,
                    skill_name=skill_name,
                    importance=importance
                )

def seed_job_companies():
    with driver.session() as session:
        for title, _, _, company in jobs:
            session.run(
                """
                MATCH (j:Job {title: $title})
                MATCH (c:Company {name: $company})
                MERGE (j)-[:OFFERED_BY]->(c)
                """,
                title=title,
                company=company
            )

def seed_skill_relationships():
    with driver.session() as session:
        for skill1, skill2 in skill_relationships:
            session.run(
                """
                MATCH (s1:Skill {name: $skill1})
                MATCH (s2:Skill {name: $skill2})
                MERGE (s1)-[:RELATED_TO]->(s2)
                """,
                skill1=skill1,
                skill2=skill2
            )

def seed_persons():
    with driver.session() as session:
        for name, email, password in persons:
            session.run(
                """
                MERGE (p:Person {name: $name})
                SET p.email = $email,
                    p.password = $password
                """,
                name=name,
                email=email,
                password=password
            )

def seed_person_skills():
    with driver.session() as session:
        for person_name, skills_list in person_skills.items():
            for skill_name, level in skills_list:
                session.run(
                    """
                    MATCH (p:Person {name: $person_name})
                    MATCH (s:Skill {name: $skill_name})
                    MERGE (p)-[:HAS_SKILL {level: $level}]->(s)
                    """,
                    person_name=person_name,
                    skill_name=skill_name,
                    level=level
                )

try:
    driver.verify_connectivity()
    print("Connected to CognoDB successfully!")

    seed_skills()
    print("Skills seeded successfully!")

    seed_companies()
    print("Companies seeded successfully!")

    seed_jobs()
    print("Jobs seeded successfully!")

    seed_job_skills()
    print("Job-skill relationships seeded successfully!")

    seed_job_companies()
    print("Job-company relationships seeded successfully!")

    seed_skill_relationships()
    print("Skill relationships seeded successfully!")

    seed_persons()
    print("People seeded successfully!")

    seed_person_skills()
    print("Person-skill relationships seeded successfully!")

finally:
    driver.close()