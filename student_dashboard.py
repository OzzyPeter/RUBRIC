from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session

import db_models
from database import get_db
from file_storage import save_upload
from schemas import JoinCourseRequest

router = APIRouter(prefix="/student-dashboard")


def get_student(db, matricno):
    student = db.query(db_models.Student).filter(db_models.Student.matricno == matricno).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found. Sign up first.")
    return student


def get_course(db, course_code):
    course = db.query(db_models.Course).filter(db_models.Course.course_code == course_code).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course does not exist")
    return course


@router.get("")
def dashboard():
    return {"message": "STUDENT DASHBOARD"}


@router.post("/join-course")
def join_course(data: JoinCourseRequest, db: Session = Depends(get_db)):
    student = get_student(db, data.matricno)
    course = get_course(db, data.course_code)

    existing = db.query(db_models.Enrollment).filter(
        db_models.Enrollment.student_id == student.id,
        db_models.Enrollment.course_id == course.id,
    ).first()

    if existing:
        return {"message": "You are already enrolled in this course."}

    enrollment = db_models.Enrollment(student_id=student.id, course_id=course.id)
    db.add(enrollment)
    db.commit()

    return {"message": f"You have joined {course.course_code}"}


@router.get("/assignments/{matricno}")
def view_assignments(matricno: str, db: Session = Depends(get_db)):
    student = get_student(db, matricno)

    course_ids = [e.course_id for e in student.enrollments]
    if not course_ids:
        return {"message": "You haven't joined any courses."}

    assignments = db.query(db_models.Assignment).filter(
        db_models.Assignment.course_id.in_(course_ids)
    ).all()

    return [
        {
            "course_code": a.course.course_code,
            "course_name": a.course.course_name,
            "title": a.title,
            "description": a.description,
            "deadline": a.deadline,
        }
        for a in assignments
    ]


@router.post("/submit-assignment")
def submit_assignment(
    matricno: str = Form(...),
    course_code: str = Form(...),
    assignment_title: str = Form(...),
    notes: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    student = get_student(db, matricno)
    course = get_course(db, course_code)

    assignment = db.query(db_models.Assignment).filter(
        db_models.Assignment.course_id == course.id,
        db_models.Assignment.title == assignment_title,
    ).first()

    if assignment is None:
        raise HTTPException(status_code=404, detail="Assignment does not exist")

    file_path, original_filename = save_upload(file, "submissions")

    submission = db.query(db_models.Submission).filter(
        db_models.Submission.assignment_id == assignment.id,
        db_models.Submission.student_id == student.id,
    ).first()

    if submission:
        # Resubmission: overwrite the existing row. (The old uploaded file
        # is left on disk, orphaned — fine for a school project, but worth
        # cleaning up if you take this further.)
        submission.file_path = file_path
        submission.original_filename = original_filename
        submission.notes = notes
        submission.status = "Resubmitted"
    else:
        submission = db_models.Submission(
            assignment_id=assignment.id,
            student_id=student.id,
            file_path=file_path,
            original_filename=original_filename,
            notes=notes,
            status="Submitted",
        )
        db.add(submission)

    db.commit()
    db.refresh(submission)

    return {
        "message": "Assignment submitted successfully",
        "status": submission.status,
        "file_url": f"/uploads/{submission.file_path}",
    }


@router.get("/submission-status/{matricno}")
def submission_status(matricno: str, db: Session = Depends(get_db)):
    student = get_student(db, matricno)
    return [{"assignment": s.assignment.title, "status": s.status} for s in student.submissions]


@router.get("/grades/{matricno}")
def view_grades(matricno: str, db: Session = Depends(get_db)):
    student = get_student(db, matricno)
    return [
        {"assignment": s.assignment.title, "grade": s.grade, "feedback": s.feedback}
        for s in student.submissions
        if s.grade is not None
    ]