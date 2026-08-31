from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Form, File, UploadFile
from sqlalchemy.orm import Session

import db_models
from database import get_db
from file_storage import save_upload
from gemini_service import generate_ai_grade
from schemas import CourseRequest, GradeRequest

router = APIRouter(prefix="/lecturer-dashboard")


def get_lecturer(db, lecturer_id):
    lecturer = db.query(db_models.Lecturer).filter(db_models.Lecturer.id == lecturer_id).first()
    if lecturer is None:
        raise HTTPException(status_code=404, detail="Lecturer not found")
    return lecturer


def get_course(db, course_code):
    course = db.query(db_models.Course).filter(db_models.Course.course_code == course_code).first()
    if course is None:
        raise HTTPException(status_code=404, detail="Course does not exist")
    return course


def get_assignment(db, course, title):
    assignment = db.query(db_models.Assignment).filter(
        db_models.Assignment.course_id == course.id,
        db_models.Assignment.title == title,
    ).first()
    if assignment is None:
        raise HTTPException(status_code=404, detail="Assignment does not exist")
    return assignment


@router.get("")
def dashboard():
    return {"message": "LECTURER DASHBOARD"}


@router.post("/create-course")
def create_course(data: CourseRequest, db: Session = Depends(get_db)):
    get_lecturer(db, data.lecturer_id)

    existing = db.query(db_models.Course).filter(db_models.Course.course_code == data.course_code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Course already exists")

    course = db_models.Course(
        course_code=data.course_code,
        course_name=data.course_name,
        lecturer_id=data.lecturer_id,
    )
    db.add(course)
    db.commit()
    db.refresh(course)

    return {"message": f"{course.course_code} created successfully"}


@router.post("/create-assignment")
def create_assignment(
    lecturer_id: int = Form(...),
    course_code: str = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    deadline: str = Form(...),
    attachment: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    get_lecturer(db, lecturer_id)
    course = get_course(db, course_code)

    if course.lecturer_id != lecturer_id:
        raise HTTPException(status_code=403, detail="You do not teach this course")

    assignment = db_models.Assignment(
        course_id=course.id,
        title=title,
        description=description,
        deadline=deadline,
    )

    if attachment is not None and attachment.filename:
        path, original_name = save_upload(attachment, "assignments")
        assignment.attachment_path = path
        assignment.attachment_filename = original_name

    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return {
        "message": "Assignment created successfully",
        "assignment": assignment.title,
        "attachment_url": f"/uploads/{assignment.attachment_path}" if assignment.attachment_path else None,
    }


@router.get("/students/{course_code}")
def view_students(course_code: str, db: Session = Depends(get_db)):
    course = get_course(db, course_code)

    students = (
        db.query(db_models.Student)
        .join(db_models.Enrollment, db_models.Enrollment.student_id == db_models.Student.id)
        .filter(db_models.Enrollment.course_id == course.id)
        .all()
    )

    return [{"name": s.first_name, "matricno": s.matricno} for s in students]


@router.get("/submissions/{course_code}/{assignment_title}")
def view_submissions(course_code: str, assignment_title: str, db: Session = Depends(get_db)):
    course = get_course(db, course_code)
    assignment = get_assignment(db, course, assignment_title)

    return [
        {
            "submission_id": s.id,
            "student": s.student.first_name,
            "matricno": s.student.matricno,
            "status": s.status,
            "notes": s.notes,
            "file_url": f"/uploads/{s.file_path}" if s.file_path else None,
            "original_filename": s.original_filename,
            "grade": s.grade,
            "feedback": s.feedback,
            "ai_grade": s.ai_grade,
            "ai_feedback": s.ai_feedback,
        }
        for s in assignment.submissions
    ]


@router.post("/ai-grade/{submission_id}")
def ai_grade_submission(submission_id: int, db: Session = Depends(get_db)):
    """Ask Gemini for a suggested grade + feedback. Doesn't finalize the
    grade — call /grade afterwards to accept or override it."""
    submission = db.query(db_models.Submission).filter(db_models.Submission.id == submission_id).first()
    if submission is None:
        raise HTTPException(status_code=404, detail="Submission not found")

    assignment = submission.assignment

    # Gemini can't read the actual uploaded file yet — it only sees the
    # filename and any notes the student typed. Good enough to sanity-check
    # a submission exists and roughly matches the assignment, not to
    # actually read code/essay content. Ask if you want real file-content
    # grading added later (it's possible, just more work).
    submission_summary = (
        f"Uploaded file: {submission.original_filename or 'none'}\n"
        f"Student notes: {submission.notes or 'none'}"
    )

    grade, feedback = generate_ai_grade(
        assignment_title=assignment.title,
        description=assignment.description,
        deadline=assignment.deadline,
        submission_content=submission_summary,
    )

    submission.ai_grade = grade
    submission.ai_feedback = feedback
    db.commit()

    return {"ai_grade": grade, "ai_feedback": feedback}


@router.post("/grade")
def grade_submission(data: GradeRequest, db: Session = Depends(get_db)):
    course = get_course(db, data.course_code)
    assignment = get_assignment(db, course, data.assignment_title)

    student = db.query(db_models.Student).filter(db_models.Student.matricno == data.matricno).first()
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    submission = db.query(db_models.Submission).filter(
        db_models.Submission.assignment_id == assignment.id,
        db_models.Submission.student_id == student.id,
    ).first()

    if submission is None:
        raise HTTPException(status_code=404, detail="Submission not found for this student")

    submission.grade = data.grade
    submission.feedback = data.feedback
    submission.status = "Graded"
    db.commit()

    return {
        "message": "Grade recorded successfully",
        "grade": submission.grade,
        "feedback": submission.feedback,
    }