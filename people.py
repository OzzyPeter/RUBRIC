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
            print(f"You have joined {course.course_code}")
        else:
            print("You are already enrolled in this course.")

    def view_assignments(self):
        for course in self.courses:
            print(f"\nAssignments for {course.course_code} - {course.course_name}")

            if not course.assignments:
                print("No assignments available.")
                continue

            for assignment in course.assignments:
                print(f"Title: {assignment.title}")
                print(f"Description: {assignment.description}")
                print(f"Deadline: {assignment.deadline}")
                print()

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
        self.assignments = []

    def create_course(self):
        course_code = input("Course code: ")
        course_name = input("Course name: ")

        course = Course(course_code, course_name, self)
        self.courses.append(course)

        print(f"{course_code} created successfully.")

    def create_assignment(self, course):
        self.course = course
        self.title = input("Assignment title: ")
        self.description = input("Assignment description: ")
        self.deadline = input("Assignment deadline: ")
        
        assignment = Assignment(self.title, self.description, self.deadline, self.course)
        self.assignments.append(assignment)


    def view_students(self, course):
        print(f"\nStudents enrolled in {course.course_code}:")

        if not course.students:
            print("No students enrolled.")
            return

        for student in course.students:
            print(f"- {student.name} ({student.matricno})")

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
        self.submissions = []
        self.assignments = []

        self.title = title
        self.description = description
        self.deadline = deadline
        self.course = course

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