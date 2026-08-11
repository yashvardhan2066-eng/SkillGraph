# SkillGraph

SkillGraph is a graph-powered career exploration web application that helps students explore jobs, skills, and personalized job matches.

The application uses CognoDB as the graph database and Flask as the web backend.

---

## Features

- Student login and session-based authentication
- Personalized student dashboard
- Explore available jobs
- View detailed job information
- Explore technical skills
- View related skills and jobs
- Personalized job matching based on student skills
- Matching and missing skill identification
- Graph-based relationship traversal
- Graceful error handling
- Responsive web interface

---

## Technology Stack

### Backend

- Python
- Flask
- Neo4j Python Driver

### Database

- CognoDB
- Cypher

### Frontend

- HTML
- CSS
- Jinja2 Templates

### Configuration

- python-dotenv
- Environment variables

---

## Graph Data Model

SkillGraph models career-related information as a graph.

### Nodes

- `Person`
- `Skill`
- `Job`
- `Company`

### Relationships

- `HAS_SKILL` — Person → Skill
- `REQUIRES` — Job → Skill
- `OFFERED_BY` — Job → Company
- `RELATED_TO` — Skill → Skill

### Relationship Properties

`HAS_SKILL` stores:

```text
level
```

Example:

```text
Person ──HAS_SKILL {level: "Intermediate"}──> Skill
```

`REQUIRES` stores:

```text
importance
```

Example:

```text
Job ──REQUIRES {importance: "Required"}──> Skill
```

---

## Example Graph

```text
Person
   │
   │ HAS_SKILL
   ▼
Skill
   ▲
   │ REQUIRES
   │
Job
   │
   │ OFFERED_BY
   ▼
Company
```

Skills can also be connected:

```text
Skill ──RELATED_TO──> Skill
```

For example:

```text
Python ──RELATED_TO──> Flask
Python ──RELATED_TO──> FastAPI
Python ──RELATED_TO──> Django
```

---

## Job Matching

The Job Matcher compares a student's existing skills with the skills required by each job.

For example:

```text
Student Skills
--------------
Python
SQL
Flask
Git

Job Requirements
----------------
Python
SQL
REST APIs
Flask
Docker
Git
```

The application identifies:

```text
Matching Skills
---------------
Python
SQL
Flask
Git

Missing Skills
--------------
REST APIs
Docker
```

The match percentage is calculated from the number of matching required skills.

This allows students to understand both:

- Jobs they currently match
- Skills they need to develop

---

## Application Flow

```text
Open SkillGraph
      ↓
    Login
      ↓
  Dashboard
      │
      ├── Explore Jobs
      │       ↓
      │   Job Details
      │
      ├── Explore Skills
      │       ↓
      │   Skill Details
      │
      └── Your Job Matches
              ↓
        Personalized Matches
```

---

## Project Architecture

```text
Browser
   │
   ▼
Flask Application
   │
   ├── Routes
   │
   └── Jinja Templates
           │
           ▼
       queries.py
           │
           ▼
    Neo4j Python Driver
           │
           ▼
        CognoDB
```

---

## Project Structure

```text
SkillGraph/
│
├── app.py
├── queries.py
├── seed.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── jobs.html
│   ├── job_details.html
│   ├── skills.html
│   ├── skill_details.html
│   ├── matches.html
│   ├── error.html
│   └── 404.html
│
└── static/
    └── css/
        └── style.css
```

---

## Setup

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd SkillGraph
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file:

```text
COGNODB_URI=your_cognodb_uri
COGNODB_USERNAME=your_username
COGNODB_PASSWORD=your_password
FLASK_SECRET_KEY=your_secret_key
```

Do not commit `.env` to GitHub.

### 5. Seed the database

```bash
python seed.py
```

You should see messages confirming that the data and relationships were created.

### 6. Run the application

```bash
python app.py
```

Open:

```text
http://127.0.0.1:8000
```

---

## Demo Accounts

The project contains demo student accounts for testing.

| Student | Email | Password |
|---|---|---|
| Arjun | arjun@example.com | arjun123 |
| Priya | priya@example.com | priya123 |
| Rahul | rahul@example.com | rahul123 |
| Ananya | ananya@example.com | ananya123 |
| Vikram | vikram@example.com | vikram123 |

These accounts are for demonstration purposes only.

---

## Sample Graph Data

The seeded dataset contains:

- 5 Persons
- 20 Skills
- 10 Jobs
- 6 Companies
- 22 Person–Skill relationships
- 44 Job–Skill requirements
- 16 Skill relationships
- 10 Job–Company relationships

---

## Error Handling

The application includes error handling for:

- Database connectivity issues
- Invalid job requests
- Invalid skill requests
- Unauthorized access
- Missing pages

A dedicated health endpoint is also available:

```text
/health
```

It verifies whether the application can connect to CognoDB.

A database connection failure is handled gracefully instead of exposing raw database errors to the user.

---

## Authentication

SkillGraph uses Flask sessions to maintain the currently logged-in student.

After successful authentication:

```text
Login
  ↓
Session created
  ↓
Dashboard
  ↓
Personalized Job Matches
```

Protected pages redirect unauthenticated users back to the login page.

Logging out clears the current session.

---

## Security Notes

Database credentials and the Flask secret key are stored using environment variables.

The `.env` file is excluded from version control using `.gitignore`.

The login accounts are demonstration accounts for this prototype and should not be considered production authentication.

---

## Graph Traversal Example

One of the graph queries explores relationships between a student's existing skills, related skills, and jobs.

Example path:

```text
Person
   ↓ HAS_SKILL
Existing Skill
   ↓ RELATED_TO
Related Skill
   ↑ REQUIRES
Job
   ↓ OFFERED_BY
Company
```

For example:

```text
Arjun
  ↓
Python
  ↓
Flask
  ↑
Backend Developer
  ↓
CloudSphere
```

This demonstrates how SkillGraph uses relationships in the graph to discover career-related connections.

---

## Future Improvements

Possible future improvements include:

- Password hashing
- User registration
- Admin dashboard
- More jobs and companies
- Job search and filtering
- Skill recommendations
- Learning-resource recommendations
- Advanced graph-based career paths
- Production authentication and authorization

---

## Author

Developed as a graph database application project using Python, Flask, and CognoDB.

> **Security reminder:** Make sure `.env` is listed in `.gitignore`. Never upload your actual `COGNODB_PASSWORD` or `COGNODB_URI` to the repository.
