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

    def view_assignments(self):
        for a in Assignment.assignment:
            return a["title"], a["description"], a["deadline"]

    def submit_assignment(self):
        pass

    def see_submission_status(self):
        pass

    def view_grades(self):
        pass

class Lecturer(People):
    def __init__(self, name):
        super().__init__(name)
        self.courses = []

    def create_course(self):
        course = input("Create Course: ")
        self.courses.append(course)

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

    def join_course(self, name):
        self.name = name
        self.students.append(self.name)

class Assignment():
    assignment = []
    submissions = []

    def __init__(self):
        pass

    @classmethod
    def create_assignment(self, title, description, deadline, course):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.course = course

        assignment = {"title": title, "description": description, "deadline": deadline, "course": course}
        Assignment.assignment.append(assignment)
        


class Submission:
    def __init__(self, student, assignment, file):
        self.student = student
        self.assignment = assignment
        self.file = file
        self.grade = None
        self.feedback = None
