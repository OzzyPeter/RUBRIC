from pydantic import BaseModel


class SignupRequest(BaseModel):
    first_name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class CourseRequest(BaseModel):
    course_code: str
    course_name: str


class AssignmentRequest(BaseModel):
    course_code: str
    title: str
    description: str
    deadline: str


class GradeRequest(BaseModel):
    course_code: str
    assignment_title: str
    matricno: str
    grade: float
    feedback: str = ""


class JoinCourseRequest(BaseModel):
    matricno: str
    name: str
    course_code: str


class SubmitAssignmentRequest(BaseModel):
    matricno: str
    course_code: str
    assignment_title: str
    file: str