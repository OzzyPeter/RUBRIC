from people import Student, Lecturer


print("""
=================
STUDENT DASHBOARD
=================
""")


# Temporary student for testing.
# Later, login() will provide these details.
student = Student(
    "Student Name",
    "MAT123456"
)


while True:

    print("""
1. Join Course
2. View Assignments
3. Submit Assignment
4. Resubmit Assignment
5. See Submission Status
6. View Grades
7. Exit
""")

    choice = input("Input choice: ")

    match choice:

        case "1":

            course_code = input(
                "Input course code: "
            ).upper()

            selected_course = None

            # Temporary:
            # Search through lecturers and their courses.
            # Later, the database will handle this.
            for lecturer in Lecturer.all_lecturers:
                for course in lecturer.courses:

                    if course.course_code == course_code:
                        selected_course = course
                        break

                if selected_course:
                    break

            if selected_course:

                student.join_course(selected_course)

            else:
                print(
                    f"{course_code} does not exist."
                )

        case "2":

            if not student.courses:
                print(
                    "You haven't joined any courses."
                )
                continue

            student.view_assignments()

        case "3":

            student.submit_assignment()

        case "4":

            pass

        case "5":

            student.see_submission_status()

        case "6":

            student.view_grades()

        case "7":

            print("Exiting student dashboard...")
            break

        case _:

            print("Invalid choice.")