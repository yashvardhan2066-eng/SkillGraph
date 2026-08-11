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

def authenticate_person(email, password):
    with driver.session() as session:
        result = session.run(
            """
            MATCH (p:Person {email: $email})
            WHERE p.password = $password
            RETURN p.name AS name,
                   p.email AS email
            """,
            email=email,
            password=password
        )

        record = result.single()

        if record:
            return record.data()

        return None

def get_all_jobs():
    with driver.session() as session:
        result = session.run(
            """
            MATCH (j:Job)-[:OFFERED_BY]->(c:Company)
            RETURN j.title AS title,
                   j.description AS description,
                   j.experience_level AS experience_level,
                   c.name AS company,
                   c.location AS location
            ORDER BY j.title
            """
        )

        return [record.data() for record in result]


def get_job_details(job_title):
    with driver.session() as session:
        result = session.run(
            """
            MATCH (j:Job {title: $job_title})
            MATCH (j)-[:REQUIRES]->(s:Skill)
            MATCH (j)-[:OFFERED_BY]->(c:Company)
            RETURN j.title AS title,
                   j.description AS description,
                   j.experience_level AS experience_level,
                   c.name AS company,
                   c.location AS location,
                   collect({
                       name: s.name,
                       category: s.category
                   }) AS skills
            """,
            job_title=job_title
        )

        record = result.single()

        if record:
            return record.data()

        return None


def get_skill_details(skill_name):
    with driver.session() as session:
        result = session.run(
            """
            MATCH (s:Skill {name: $skill_name})
            OPTIONAL MATCH (s)-[:RELATED_TO]->(related:Skill)
            OPTIONAL MATCH (j:Job)-[:REQUIRES]->(s)
            RETURN s.name AS name,
                   s.category AS category,
                   collect(DISTINCT related.name) AS related_skills,
                   collect(DISTINCT j.title) AS jobs
            """,
            skill_name=skill_name
        )

        record = result.single()

        if record:
            return record.data()

        return None


def get_jobs_for_person(person_name):
    with driver.session() as session:
        result = session.run(
            """
            MATCH (p:Person {name: $person_name})-[:HAS_SKILL]->(user_skill:Skill)

            MATCH (j:Job)-[:REQUIRES]->(required_skill:Skill)

            WITH j,
                 collect(DISTINCT user_skill.name) AS user_skills,
                 collect(DISTINCT required_skill.name) AS required_skills

            WITH j,
                 required_skills,
                 [skill IN required_skills
                  WHERE skill IN user_skills] AS matching_skills

            WITH j,
                 required_skills,
                 matching_skills,
                 [skill IN required_skills
                  WHERE NOT skill IN matching_skills] AS missing_skills

            MATCH (j)-[:OFFERED_BY]->(c:Company)

            RETURN
                j.title AS job,
                c.name AS company,
                matching_skills,
                missing_skills,
                size(matching_skills) AS matching_count,
                size(required_skills) AS required_count,
                100.0 * size(matching_skills) / size(required_skills)
                    AS match_percentage

            ORDER BY match_percentage DESC
            """,
            person_name=person_name
        )

        return [record.data() for record in result]

def get_related_job_paths(person_name):
    with driver.session() as session:
        result = session.run(
            """
            MATCH (p:Person {name: $person_name})-[:HAS_SKILL]->(s1:Skill)
                  -[:RELATED_TO]->(s2:Skill)
                  <-[:REQUIRES]-(j:Job)
            MATCH (j)-[:OFFERED_BY]->(c:Company)
            RETURN DISTINCT
                   j.title AS job,
                   c.name AS company,
                   s1.name AS existing_skill,
                   s2.name AS related_skill
            ORDER BY job
            """,
            person_name=person_name
        )

        return [record.data() for record in result]


def close_driver():
    driver.close()


if __name__ == "__main__":
    try:
        driver.verify_connectivity()
        print("Connected to CognoDB successfully!\n")

        print("=== ALL JOBS ===")
        jobs = get_all_jobs()
        for job in jobs:
            print(job)

        print("\n=== BACKEND DEVELOPER ===")
        job = get_job_details("Backend Developer")
        print(job)

        print("\n=== PYTHON ===")
        skill = get_skill_details("Python")
        print(skill)

        print("\n=== JOBS FOR ARJUN ===")
        jobs_for_arjun = get_jobs_for_person("Arjun")
        for job in jobs_for_arjun:
            print(job)

        print("\n=== RELATED JOB PATHS FOR ARJUN ===")
        paths = get_related_job_paths("Arjun")
        for path in paths:
            print(path)

    finally:
        close_driver()