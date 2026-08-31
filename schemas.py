from pydantic import BaseModel, EmailStr, Field


class StudentSignupRequest(BaseModel):
    first_name: str
    email: EmailStr
    password: str = Field(min_length=8)
    matricno: str


class LecturerSignupRequest(BaseModel):
    first_name: str
    email: EmailStr
    password: str = Field(min_length=8)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class CourseRequest(BaseModel):
    lecturer_id: int
    course_code: str
    course_name: str


class GradeRequest(BaseModel):
    course_code: str
    assignment_title: str
    matricno: str
    grade: float
    feedback: str = ""


class JoinCourseRequest(BaseModel):
    matricno: str
    course_code: str