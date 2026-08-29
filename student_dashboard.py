from fastapi import APIRouter, HTTPException

from people import Student, Lecturer
from models import JoinCourseRequest, SubmitAssignmentRequest

router = APIRouter(prefix="/student-dashboard")


def get_or_create_student(matricno, name):
    if matricno in Student.all_students:
        return Student.all_students[matricno]
    return Student(name, matricno)


def find_course_anywhere(course_code):
    for lecturer in Lecturer.all_lecturers:
        for course in lecturer.courses:
            if course.course_code == course_code:
                return course
    return None


@router.get("")
def dashboard():
    return {"message": "STUDENT DASHBOARD"}


@router.post("/join-course")
def join_course(data: JoinCourseRequest):
    course = find_course_anywhere(data.course_code)

    if course is None:
        raise HTTPException(status_code=404, detail=f"{data.course_code} does not exist")

    student = get_or_create_student(data.matricno, data.name)

    return student.join_course(course)


@router.get("/assignments/{matricno}")
def view_assignments(matricno: str):
    student = Student.all_students.get(matricno)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    if not student.courses:
        return {"message": "You haven't joined any courses."}

    return student.view_assignments()


@router.post("/submit-assignment")
def submit_assignment(data: SubmitAssignmentRequest):
    student = Student.all_students.get(data.matricno)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found. Join a course first.")

    course = find_course_anywhere(data.course_code)

    if course is None:
        raise HTTPException(status_code=404, detail="Course does not exist")

    assignment = None
    for a in course.assignments:
        if a.title == data.assignment_title:
            assignment = a
            break

    if assignment is None:
        raise HTTPException(status_code=404, detail="Assignment does not exist")

    submission = student.submit_assignment(assignment, data.file)

    return {
        "message": "Assignment submitted successfully",
        "status": submission.status
    }


@router.get("/submission-status/{matricno}")
def submission_status(matricno: str):
    student = Student.all_students.get(matricno)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student.see_submission_status()


@router.get("/grades/{matricno}")
def view_grades(matricno: str):
    student = Student.all_students.get(matricno)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student.view_grades()