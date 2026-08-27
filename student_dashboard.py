from people import Lecturer, Student, Assignment, Course

print("""
=================
STUDENT DASHBOARD
=================
""")

while True:
    print("""
1. Join course
2. View Assignments
3. Submit Assignment
4. Resubmit Assignment
5. See Submission Status
6. View Grades
""")

    choice = input("Input choice: ")

    student = Student("from login name", "from matric number(login)")
    course1 = Course("from login")

    joined_courses = []

    match choice:
     
        case "1":
            course = input("Input course to join: ").lower()

            if course in Lecturer.courses:

                course1.join_course()

                joined_courses.append(course)

            else:
                print(f"{course} does not exist")
                

        case "2":
            course = input("Input course to view assignment: ").lower()

            if course in joined_courses:
                student.view_assignments()

                if student.view_assignments() == []:
                    print("No assignments available for this course")
                
            else:
                print("You haven't joined this course")

        case "3":
            pass

        case "4":
            pass

        case "5":
            pass