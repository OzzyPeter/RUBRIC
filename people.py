class People:
    def __init__(self, name):
        self.name = name


def create_account(self):
    pass

def login(self):
    pass

class Student(People):
    def __init__(self, name, matricno):
        super().__init__(name)
        self.matricno = matricno
        self.courses = []
        self.submissions = []

def join_course(self, course):
    if course not in self.courses:
        self.courses.append(course)
        course.students.append(self)

        return {
            "message": f"You have joined {course.course_code}"
        }

    return {
        "message": "You are already enrolled in this course."
    }

def view_assignments(self):
    assignments = []

    for course in self.courses:
        for assignment in course.assignments:
            assignments.append({
                "course_code": course.course_code,
                "course_name": course.course_name,
                "title": assignment.title,
                "description": assignment.description,
                "deadline": assignment.deadline
            })

    return assignments

def submit_assignment(self, assignment, file):
    submission = Submission(
        student=self,
        assignment=assignment,
        file=file
    )

    return submission

def see_submission_status(self):
    return [
        {
            "assignment": submission.assignment.title,
            "status": submission.status
        }
        for submission in self.submissions
    ]

def view_grades(self):
    return [
        {
            "assignment": submission.assignment.title,
            "grade": submission.grade,
            "feedback": submission.feedback
        }
        for submission in self.submissions
        if submission.grade is not None
    ]

class Lecturer(People):
    def __init__(self, name):
        super().__init__(name)
        self.courses = []
        self.assignments = []

def create_course(self, course_code, course_name):
    course = Course(
        course_code=course_code,
        course_name=course_name,
        lecturer=self
    )

    self.courses.append(course)

    return course

def create_assignment(
    self,
    course,
    title,
    description,
    deadline
):
    assignment = Assignment(
        title=title,
        description=description,
        deadline=deadline,
        course=course
    )

    self.assignments.append(assignment)
    course.assignments.append(assignment)

    return assignment

def view_students(self, course):
    return [
        {
            "name": student.name,
            "matricno": student.matricno
        }
        for student in course.students
    ]

def set_submission_requirements(self):
    pass

def view_submissions(self):
    pass

def grade_manually(self):
    pass

def ai_assisted_grading(self):
    pass

def review_ai_grades(self):
    pass

def release_grades(self):
    pass


class Course:
    def __init__(self, course_code, course_name, lecturer):
        self.course_code = course_code
        self.course_name = course_name
        self.lecturer = lecturer
        
        self.students = []
        self.assignments = []

class Assignment:
    def __init__(self, title, description, deadline, course):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.course = course

        self.submissions = []

class Submission:
    def __init__(self, student, assignment, file):
        self.student = student
        self.assignment = assignment
        self.file = file
        self.grade = None
        self.feedback = None
        self.status = "Submitted"

        assignment.submissions.append(self)
        student.submissions.append(self)

