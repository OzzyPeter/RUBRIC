import os

from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

import db_models
from database import Base, engine, get_db
from lecturer_dashboard import router as lecturer_router
from student_dashboard import router as student_router
from schemas import LoginRequest, StudentSignupRequest, LecturerSignupRequest
from security import hash_password, verify_password

Base.metadata.create_all(bind=engine)

os.makedirs("uploads/assignments", exist_ok=True)
os.makedirs("uploads/submissions", exist_ok=True)

app = FastAPI()
app.include_router(lecturer_router)
app.include_router(student_router)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


@app.get("/")
def root():
    return {"message": "something"}


@app.post("/signup/student")
def signup_student(data: StudentSignupRequest, db: Session = Depends(get_db)):
    if db.query(db_models.Student).filter(db_models.Student.email == data.email).first():
        return {"message": "Account already exists"}

    if db.query(db_models.Student).filter(db_models.Student.matricno == data.matricno).first():
        raise HTTPException(status_code=400, detail="This matric number is already registered")

    student = db_models.Student(
        first_name=data.first_name,
        email=data.email,
        password_hash=hash_password(data.password),
        matricno=data.matricno,
    )
    db.add(student)
    db.commit()
    db.refresh(student)

    return {"message": "Account creation successful", "user_id": student.id, "role": "student"}


@app.post("/signup/lecturer")
def signup_lecturer(data: LecturerSignupRequest, db: Session = Depends(get_db)):
    if db.query(db_models.Lecturer).filter(db_models.Lecturer.email == data.email).first():
        return {"message": "Account already exists"}

    lecturer = db_models.Lecturer(
        first_name=data.first_name,
        email=data.email,
        password_hash=hash_password(data.password),
    )
    db.add(lecturer)
    db.commit()
    db.refresh(lecturer)

    return {"message": "Account creation successful", "user_id": lecturer.id, "role": "lecturer"}


@app.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    student = db.query(db_models.Student).filter(db_models.Student.email == data.email).first()
    if student:
        if not verify_password(data.password, student.password_hash):
            return {"message": "incorrect password"}
        return {
            "message": "login successful",
            "user_id": student.id,
            "role": "student",
            "first_name": student.first_name,
            "matricno": student.matricno,
        }

    lecturer = db.query(db_models.Lecturer).filter(db_models.Lecturer.email == data.email).first()
    if lecturer:
        if not verify_password(data.password, lecturer.password_hash):
            return {"message": "incorrect password"}
        return {
            "message": "login successful",
            "user_id": lecturer.id,
            "role": "lecturer",
            "first_name": lecturer.first_name,
        }

    raise HTTPException(status_code=404, detail="user not found")