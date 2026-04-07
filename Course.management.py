# Course Management System

students = []
courses = []
enrollments = []

# ---------------- ADD FUNCTIONS ----------------
def add_student():
    sid = input("Enter Student ID: ")
    name = input("Enter Student Name: ")
    students.append({"id": sid, "name": name})
    print("Student added!\n")

def add_course():
    cid = input("Enter Course ID: ")
    name = input("Enter Course Name: ")
    courses.append({"id": cid, "name": name})
    print("Course added!\n")

def enroll_student():
    sid = input("Enter Student ID: ")
    cid = input("Enter Course ID: ")

    if not any(s["id"] == sid for s in students):
        print("Student not found!\n")
        return
    if not any(c["id"] == cid for c in courses):
        print("Course not found!\n")
        return

    enrollments.append({"student_id": sid, "course_id": cid})
    print("Enrollment successful!\n")

# ---------------- UPDATE FUNCTIONS ----------------
def update_student():
    sid = input("Enter Student ID to update: ")
    for s in students:
        if s["id"] == sid:
            new_name = input("Enter new name: ")
            s["name"] = new_name
            print("Student updated!\n")
            return
    print("Student not found!\n")

def update_course():
    cid = input("Enter Course ID to update: ")
    for c in courses:
        if c["id"] == cid:
            new_name = input("Enter new course name: ")
            c["name"] = new_name
            print("Course updated!\n")
            return
    print("Course not found!\n")

def update_enrollment():
    sid = input("Enter Student ID: ")
    old_cid = input("Enter Old Course ID: ")

    for e in enrollments:
        if e["student_id"] == sid and e["course_id"] == old_cid:
            new_cid = input("Enter New Course ID: ")

            if not any(c["id"] == new_cid for c in courses):
                print("New course not found!\n")
                return

            e["course_id"] = new_cid
            print("Enrollment updated!\n")
            return
    print("Enrollment not found!\n")

# ---------------- DELETE FUNCTIONS ----------------
def delete_student():
    sid = input("Enter Student ID: ")
    global enrollments

    for s in students:
        if s["id"] == sid:
            students.remove(s)
            enrollments = [e for e in enrollments if e["student_id"] != sid]
            print("Student deleted!\n")
            return
    print("Student not found!\n")

def delete_course():
    cid = input("Enter Course ID: ")
    global enrollments

    for c in courses:
        if c["id"] == cid:
            courses.remove(c)
            enrollments = [e for e in enrollments if e["course_id"] != cid]
            print("Course deleted!\n")
            return
    print("Course not found!\n")

def delete_enrollment():
    sid = input("Enter Student ID: ")
    cid = input("Enter Course ID: ")

    for e in enrollments:
        if e["student_id"] == sid and e["course_id"] == cid:
            enrollments.remove(e)
            print("Enrollment deleted!\n")
            return
    print("Enrollment not found!\n")

# ---------------- VIEW FUNCTIONS ----------------
def view_students():
    print("\nStudents:")
    for s in students:
        print(s)
    print()

def view_courses():
    print("\nCourses:")
    for c in courses:
        print(c)
    print()

def view_enrollments():
    print("\nEnrollments:")
    for e in enrollments:
        print(e)
    print()

# ---------------- MENU ----------------
def menu():
    while True:
        print("===== Course Management System =====")
        print("1. Add Student")
        print("2. Add Course")
        print("3. Enroll Student")
        print("4. View Students")
        print("5. View Courses")
        print("6. View Enrollments")
        print("7. Update Student")
        print("8. Update Course")
        print("9. Update Enrollment")
        print("10. Delete Student")
        print("11. Delete Course")
        print("12. Delete Enrollment")
        print("13. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            add_student()
        elif choice == '2':
            add_course()
        elif choice == '3':
            enroll_student()
        elif choice == '4':
            view_students()
        elif choice == '5':
            view_courses()
        elif choice == '6':
            view_enrollments()
        elif choice == '7':
            update_student()
        elif choice == '8':
            update_course()
        elif choice == '9':
            update_enrollment()
        elif choice == '10':
            delete_student()
        elif choice == '11':
            delete_course()
        elif choice == '12':
            delete_enrollment()
        elif choice == '13':
            print("Exiting...")
            break
        else:
            print("Invalid choice!\n")

# Run program
menu()