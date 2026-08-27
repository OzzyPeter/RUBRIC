from people import Lecturer, Assignment


print("==================")
print("LECTURER DASHBOARD")
print("==================")


lecturer = Lecturer("Adebisi")


while True:

    print("""
1. Create Course
2. Create Assignment
3. View Students
4. View Submissions
5. Grade Assignment
6. AI Assisted Grading
7. Release Grades
8. Exit
""")

    choice = input("Input choice: ")

    match choice:

        case "1":
            lecturer.create_course()

        case "2":
            if not lecturer.courses:
                print("You haven't created any courses yet.")
                continue

            print("\nYour courses:")

            for course in lecturer.courses:
                print(f"- {course.course_code}: {course.course_name}")

            course_code = input(
                "\nSelect course to create assignment: "
            ).upper()

            selected_course = None

            for course in lecturer.courses:
                if course.course_code == course_code:
                    selected_course = course
                    break

            if selected_course is None:
                print("Course does not exist.")
                continue

            title = input("Assignment title: ")
            description = input("Assignment description: ")
            deadline = input("Assignment deadline: ")

            Assignment(
                title,
                description,
                deadline,
                selected_course
            )

            print("Assignment created successfully.")

        case "3":
            if not lecturer.courses:
                print("You haven't created any courses yet.")
                continue

            print("\nYour courses:")

            for course in lecturer.courses:
                print(f"- {course.course_code}: {course.course_name}")

            course_code = input(
                "\nSelect course to view students: "
            ).upper()

            selected_course = None

            for course in lecturer.courses:
                if course.course_code == course_code:
                    selected_course = course
                    break

            if selected_course:
                lecturer.view_students(selected_course)
            else:
                print("Course does not exist.")

        case "4":
            pass

        case "5":
            pass

        case "6":
            pass

        case "7":
            pass

        case "8":
            print("Exiting lecturer dashboard...")
            break

        case _:
            print("Invalid choice.")