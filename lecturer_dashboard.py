from fastapi import APIRouter, HTTPException

from people import Lecturer
from models import CourseRequest, AssignmentRequest, GradeRequest

router = APIRouter(prefix="/lecturer-dashboard")

lecturer = Lecturer("Adebisi")


def find_course(course_code):
    for course in lecturer.courses:
        if course.course_code == course_code:
            return course
    return None


def find_assignment(course, title):
    for assignment in course.assignments:
        if assignment.title == title:
            return assignment
    return None


@router.get("")
def dashboard():
    return {"message": "LECTURER DASHBOARD"}


@router.post("/create-course")
def create_course(data: CourseRequest):
    if find_course(data.course_code):
        raise HTTPException(status_code=400, detail="Course already exists")

    course = lecturer.create_course(
        data.course_code,
        data.course_name
    )

    return {
        "message": f"{course.course_code} created successfully"
    }


@router.post("/create-assignment")
def create_assignment(data: AssignmentRequest):
    selected_course = find_course(data.course_code)

    if selected_course is None:
        raise HTTPException(status_code=404, detail="Course does not exist")

    assignment = lecturer.create_assignment(
        selected_course,
        data.title,
        data.description,
        data.deadline
    )

    return {
        "message": "Assignment created successfully",
        "assignment": assignment.title
    }


@router.get("/students/{course_code}")
def view_students(course_code: str):
    course = find_course(course_code)

    if course is None:
        raise HTTPException(status_code=404, detail="Course does not exist")

    return lecturer.view_students(course)


@router.get("/submissions/{course_code}/{assignment_title}")
def view_submissions(course_code: str, assignment_title: str):
    course = find_course(course_code)

    if course is None:
        raise HTTPException(status_code=404, detail="Course does not exist")

    assignment = find_assignment(course, assignment_title)

    if assignment is None:
        raise HTTPException(status_code=404, detail="Assignment does not exist")

    return lecturer.view_submissions(assignment)


@router.post("/grade")
def grade_submission(data: GradeRequest):
    course = find_course(data.course_code)

    if course is None:
        raise HTTPException(status_code=404, detail="Course does not exist")

    assignment = find_assignment(course, data.assignment_title)

    if assignment is None:
        raise HTTPException(status_code=404, detail="Assignment does not exist")

    submission = None
    for s in assignment.submissions:
        if s.student.matricno == data.matricno:
            submission = s
            break

    if submission is None:
        raise HTTPException(status_code=404, detail="Submission not found for this student")

    lecturer.grade_manually(submission, data.grade, data.feedback)

    return {
        "message": "Grade recorded successfully",
        "grade": submission.grade,
        "feedback": submission.feedback
    }