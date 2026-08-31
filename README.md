# RUBRIC

## AI-Powered Assignment Submission and Grading Platform

**RUBRIC** is a web-based assignment submission and grading platform designed to make the assignment workflow easier for both students and lecturers.

The platform allows lecturers to create and manage assignments while students can submit their work through a centralized system. RUBRIC is also being designed to support AI-assisted grading, allowing lecturers to receive automated grading assistance based on assignment requirements and uploaded learning materials.

> 🚧 **Project Status: In Development**
>
> RUBRIC is currently under active development. The core backend and database structure are being built, and additional features are still being implemented.

---

## The Problem

Managing assignments can involve multiple platforms and manual processes. Students may submit assignments through email, messaging platforms, or forms, while lecturers must manually organize submissions and grade them.

RUBRIC aims to provide a centralized platform where:

* Lecturers can create and manage assignments.
* Students can view and submit assignments.
* Submissions can be organized and managed in one place.
* Lecturers can manually grade student submissions.
* AI-assisted grading can help provide feedback and evaluate assignments.

---

## Features

### Currently Implemented / In Development

* User account structure for students and lecturers.
* Student and lecturer roles.
* Course management.
* Assignment creation and management.
* Assignment submission structure.
* FastAPI backend.
* PostgreSQL database integration.
* SQLAlchemy ORM for database operations.
* API request and response handling.
* Backend project structure using Python and object-oriented programming principles.

### Planned Features

* User authentication and authorization.
* Secure password hashing.
* JWT authentication.
* Student assignment submission.
* Lecturer assignment grading.
* Manual grading and feedback.
* AI-assisted assignment grading.
* Multiple AI grading strictness levels.
* Uploading learning materials to provide context for AI grading.
* AI-generated feedback for student submissions.
* AI-generated assignment analysis.
* Detection tools to help lecturers identify potentially AI-generated submissions.
* Frontend integration.
* Improved validation and error handling.

---

## Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL

### Database

* PostgreSQL
* SQLAlchemy ORM

### Planned / Additional Technologies

* React
* JavaScript
* HTML
* CSS
* AI APIs for grading and feedback
* JWT Authentication

---

## Project Structure

```text
RUBRIC/
│
├── app/
│   ├── main.py
│   ├── models/
│   ├── schemas/
│   ├── routes/
│   ├── services/
│   └── database/
│
├── requirements.txt
├── README.md
└── .gitignore
```

> The project structure may change as development continues.

---

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
```

### 2. Navigate into the project directory

```bash
cd RUBRIC
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

**Windows:**

```bash
venv\Scripts\activate
```

**macOS/Linux:**

```bash
source venv/bin/activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure the database

Create a PostgreSQL database and configure your database connection using environment variables or your project's configuration settings.

### 7. Run the FastAPI application

```bash
uvicorn app.main:app --reload
```

The API should then be available locally.

FastAPI's interactive API documentation can typically be accessed at:

```text
/docs
```

---

## Current Development Progress

The project has progressed beyond the initial planning stage.

The backend architecture and core system concepts have been implemented using FastAPI, PostgreSQL, SQL, and SQLAlchemy. Current development is focused on expanding the application's functionality, connecting the different components of the system, and implementing authentication, assignment workflows, and grading features.

---

## Future Improvements

* Complete the authentication system.
* Implement role-based authorization.
* Complete assignment submission workflows.
* Implement lecturer grading workflows.
* Integrate AI-assisted grading.
* Improve API validation and error handling.
* Develop and integrate the frontend.
* Add automated testing.
* Deploy the application.

---

## Learning Goals

RUBRIC is also a project through which I am strengthening my backend development skills and gaining practical experience with:

* Building REST APIs with FastAPI.
* Designing backend application architecture.
* Working with relational databases.
* Writing SQL queries.
* Using PostgreSQL.
* Using SQLAlchemy as an ORM.
* Designing API request and response models.
* Applying object-oriented programming concepts.
* Building real-world backend workflows.

---

## Author

**Ozioma Peter**

Backend Developer focused on building scalable applications using Python, FastAPI, PostgreSQL, and modern backend technologies.

---

## Project Status

🚧 **Actively under development**

RUBRIC is a work in progress, and new features and improvements are continuously being added.
