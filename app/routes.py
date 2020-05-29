from flask import render_template, redirect, url_for, request, session
from app import app
from app.forms import TeacherForm, StudentForm, AssignmentForm, CourseForm, SubmissionForm
from psycopg2 import sql, extras, pool
from urllib.parse import urlparse
import numpy as np

app.secret_key = "cleverpassword"

result = urlparse(app.config['DATABASE_URL'])

username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname
port = result.port
print(username, password, database, hostname, port)

db_pool = pool.ThreadedConnectionPool(
    1,
    20,
    database=database,
    user=username,
    password=password,
    host=hostname,
    port=port)

def handle_login():
    if 'user' not in session:
        db_conn = db_pool.getconn()
        cursor = db_conn.cursor()

        cursor.execute('SELECT teacher_id, first_name, last_name FROM teacher')
        row = cursor.fetchone()
        session['user'] = {'id': row[0], 'name': '{} {}'.format(row[1], row[2])}

        cursor.close()
        db_pool.putconn(db_conn)

def get_teachers():
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    cursor.execute('SELECT teacher_id, first_name, last_name FROM teacher')
    rows = [{'id': c[0], 'name': '{} {}'.format(c[1], c[2])} for c in cursor]
    session['teachers'] = rows

    cursor.close()
    db_pool.putconn(db_conn)

@app.before_request
def before_request():
    handle_login()
    get_teachers()

@app.route('/gradebook/<course_id>')
def gradebook(course_id):
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()
    cursor.execute(f"SELECT * FROM course WHERE course_id = {course_id};")
    course = cursor.fetchall()[0]
    course = {
        'course_id': course[0],
        'title': course[1].strip(),
        'section': course[2],
        'department': course[3],
        'description': course[4],
        'units': course[5],
        'teacher': course[6]
    }

    cursor.execute(f"SELECT * "
                   f"FROM student "
                   f"INNER JOIN student_course ON student_course.student_id = student.student_id "
                   f"WHERE student_course.course_id = {course['course_id']}")

    studentlist = cursor.fetchall()
    students = []
    for student in studentlist:
        students.append({'student_id': student[0], 'first_name': student[1].strip(), 'last_name': student[2].strip(), 'year': student[3], 'email': student[4].strip(), 'telephone': student[5] })

    cursor.execute(f"SELECT * FROM assignment WHERE course = {course['course_id']};")
    assignmentlist = cursor.fetchall()
    assignments = []
    for assignment in assignmentlist:
        assignments.append({'assignment_id': assignment[0], 'title': assignment[1].strip(), 'description': assignment[2].strip(), 'due': assignment[3], 'points': assignment[4] })

    grades = np.zeros((max(len(students), 1), max(len(assignments), 1)))
    for i, assignment in enumerate(assignments):
        for j, student in enumerate(students):
            cursor.execute(f"SELECT student.student_id, assignment.assignment_id, submission.grade "
                           f"FROM student "
                           f"LEFT OUTER JOIN student_submission ON student.student_id = student_submission.student_id "
                           f"LEFT OUTER JOIN submission ON student_submission.submission_id = submission.submission_id "
                           f"LEFT OUTER JOIN assignment ON submission.assignment = assignment.assignment_id "
                           f"WHERE student.student_id = {student['student_id']} "
                           f"AND assignment.assignment_id = {assignment['assignment_id']};")
            results = cursor.fetchall()
            if len(results):
                grades[j, i] = results[0][2]
            else:
                grades[j, i] = None

    cursor.close()
    db_pool.putconn(db_conn)

    addStudentForm = StudentForm()
    addAssignmentForm = AssignmentForm()
    return render_template('gradebook.html', addStudentForm=addStudentForm, addAssignmentForm=addAssignmentForm, course=course, students=students, assignments=assignments, grades=grades)

### About Tab
@app.route("/about")
def about():
    return render_template("about.html")

### Add New Student Form
@app.route('/addstudent/<course_id>', methods=['GET', 'POST'])
def addStudent(course_id):

    addStudentForm = StudentForm()
    return render_template('addstudent.html', addStudentForm=addStudentForm, course_id=course_id)

### Save Add Student
@app.route('/saveAddStudent/<course_id>', methods=['POST'])
def saveAddStudent(course_id):

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    telephone = request.form['telephone']
    year = request.form['year']

    newstudent = {"first_name": first_name, "last_name": last_name, "email": email, "telephone": telephone, "year": year}
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()
    sql = f'''INSERT INTO student (first_name, last_name, email, telephone, year) VALUES (%s, %s, %s, %s, %s) RETURNING student_id AS last_id;;'''
    cursor.execute(sql,
                (newstudent['first_name'],
                 newstudent["last_name"],
                 newstudent["email"],
                 newstudent["telephone"],
                 newstudent["year"]))

    db_conn.commit()

    student_id = cursor.fetchall()[0][0]
    sql = f'''INSERT INTO student_course (student_id, course_id) VALUES (%s, %s);'''
    cursor.execute(sql, (student_id, course_id))
    db_conn.commit()
    cursor.close()

    db_pool.putconn(db_conn)
    return redirect(url_for('gradebook', course_id=course_id))


### Edit Student Form
@app.route('/editstudent/<student_id>/<course_id>', methods=['GET', 'POST'])
def editStudent(student_id, course_id):
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()
    cursor.execute(f"SELECT * "
                   f"FROM student "
                   f"INNER JOIN student_course ON student_course.student_id = student.student_id "
                   f"INNER JOIN course on course.course_id = student_course.course_id "
                   f"INNER JOIN teacher on course.teacher = teacher.teacher_id "
                   f"WHERE student.student_id = {student_id}")
    results = cursor.fetchall()
    if len(results):
        student = results[0]
        student = {'student_id': student[0], 'first_name': student[1].strip(), 'last_name': student[2].strip(),
                   'year': student[3], 'email': student[4].strip(), 'telephone': student[5]}
        courses = [{'course_id': result[8], 'coursename': result[9].strip(), 'teacher_id': result[15], 'teacher': result[16] + ' ' + result[17]} for result in results]
        student['courses'] = courses
    else:
        cursor.execute(f"SELECT * FROM student WHERE student_id={student_id};")
        student = cursor.fetchall()[0]
        student = {'student_id': student[0], 'first_name': student[1].strip(), 'last_name': student[2].strip(),
                   'year': student[3], 'email': student[4].strip(), 'telephone': student[5]}

    cursor.close()
    db_pool.putconn(db_conn)

    editStudentForm = StudentForm()
    return render_template('editstudent.html', editStudentForm=editStudentForm, student=student, course_id=course_id)

### Save Student Edits
@app.route('/saveEditStudent/<first_name>/<last_name>/<year>/<email>/<telephone>/<student_id>/<course_id>', methods=['POST'])
def saveEditStudent(first_name, last_name, year, email, telephone, student_id, course_id):

    student = {}
    form_first_name = request.form['first_name']
    form_last_name = request.form['last_name']
    form_email = request.form['email']
    form_telephone = request.form['telephone']
    form_year = request.form['year']

    # if the user changed any of these, replace them in database
    if form_first_name:
        student["first_name"] = form_first_name
    else:
        student["first_name"] = first_name
    if form_last_name:
        student["last_name"] = form_last_name
    else:
        student["last_name"] = last_name
    if form_year:
        student["year"] = form_year
    else:
        student["year"] = year
    if form_email:
        student["email"] = form_email
    else:
        student["email"] = email
    if form_telephone:
        if form_telephone == "0":
            student["telephone"] = ""
        else:
            student["telephone"] = form_telephone
    else:
        student["telephone"] = telephone
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()
    sql = f'''UPDATE student SET first_name = %s, last_name = %s, year = %s, email = %s, telephone = %s WHERE student_id = %s;'''
    cursor.execute(sql,
                (student['first_name'],
                 student['last_name'],
                 student['year'],
                 student['email'],
                 student['telephone'],
                 student_id))
    db_conn.commit()
    cursor.close()
    db_pool.putconn(db_conn)
    return redirect(url_for('gradebook', course_id=course_id))

### Delete Student
@app.route('/deleteStudent/<student_id>/<course_id>', methods=['POST'])
def deleteStudent(student_id, course_id):
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()
    sql = f'''DELETE FROM student_course WHERE student_id={student_id} and course_id={course_id};'''
    cursor.execute(sql)
    db_conn.commit()
    cursor.close()
    db_pool.putconn(db_conn)

    return redirect(url_for('gradebook', course_id=course_id))

### Add New Assignment Form
@app.route('/addassignment/<course>', methods=['GET', 'POST'])
def addAssignment(course):
    db_conn = db_pool.getconn()
    dict_cur = db_conn.cursor(cursor_factory=extras.DictCursor)

    # set the course dropdown
    addAssignmentForm = AssignmentForm()
    dict_cur.execute('SELECT course_id, title FROM course')
    choices = [(row['course_id'], row['title']) for row in dict_cur]
    choices.append(('', 'NULL'))
    addAssignmentForm.course.choices = choices

    dict_cur.close()
    db_pool.putconn(db_conn)

    return render_template('addassignment.html', addAssignmentForm=addAssignmentForm, course_id=course)

### Save Add Assignment
@app.route('/saveAddAssignment', methods=['POST'])
def saveAddAssignment():

    title = request.form['title']
    due = request.form['due']
    points = request.form['points']
    description = request.form['description']
    course = request.form['course'] or None

    newassignment = {
        "title": title,
        "due": due,
        "points": points,
        "description": description,
        "course": course
        }

    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()
    sql = f'''INSERT INTO assignment
    (title, due, points, description, course)
    VALUES (%s, %s, %s, %s, %s);'''
    cursor.execute(sql,
                (newassignment['title'],
                 str(newassignment["due"]),
                 str(newassignment["points"]),
                 newassignment["description"],
                 newassignment["course"]))

    db_conn.commit()
    cursor.close()
    db_pool.putconn(db_conn)
    return redirect(url_for('gradebook', course_id=course))

### Edit Assignment Form
@app.route('/editassignment/<assignment_id>', methods=['GET', 'POST'])
def editAssignment(assignment_id):
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    cursor.execute(f"SELECT assignment.assignment_id, assignment.title, "
                   f"assignment.description, assignment.due, assignment.points, "
                   f"assignment.course, "
                   f"student.first_name, student.last_name, student.student_id, submission.grade, submission.submitted "
                   f"FROM assignment "
                   f"INNER JOIN submission ON assignment.assignment_id = submission.assignment "
                   f"INNER JOIN student_submission on submission.submission_id = student_submission.submission_id "
                   f"INNER JOIN student on student_submission.student_id = student.student_id "
                   f"INNER JOIN course on assignment.course = course.course_id "
                   f"WHERE assignment.assignment_id = {assignment_id}")
    results = cursor.fetchall()
    if len(results):
        result = results[0]
        assignment = {
            'assignment_id': result[0],
            'title': result[1].strip(),
            'description': result[2].strip(),
            'due': result[3],
            'points': result[4],
            'course': result[5]
            }
        submissions = [{'timestamp': result[10], 'grade': result[9], 'student_id': result[8],
                        'studentname': result[6].strip() + ' ' + result[7].strip()} for result in results]
        assignment['submissions'] = submissions
    else:
        cursor.execute(f"SELECT * FROM assignment WHERE assignment_id={assignment_id};")
        assignment = cursor.fetchall()[0]
        assignment = {
            'assignment_id': assignment[0],
            'title': assignment[1].strip(),
            'description': assignment[2].strip(),
            'due': assignment[3],
            'points': assignment[4],
            'course': assignment[5]
        }


    # set the course dropdown
    editAssignmentForm = AssignmentForm()
    # cursor.execute('SELECT course_id, title FROM course;')
    # choices = [(row[0], row[1]) for row in cursor]
    # choices.append(('', 'NULL'))
    # editAssignmentForm.course.choices = choices
    # cursor.execute('SELECT course FROM assignment WHERE assignment_id= %s', assignment_id)
    # editAssignmentForm.course.default = cursor.fetchone()[0] or ''
    # editAssignmentForm.process()

    cursor.close()
    db_pool.putconn(db_conn)

    return render_template('editassignment.html', editAssignmentForm=editAssignmentForm, assignment=assignment)

### Save Assignment Edits
@app.route('/saveEditAssignment/<title>/<description>/<due>/<points>/<assignment_id>', methods=['POST'])
def saveEditAssignment(title, description, due, points, assignment_id):

    form_title = request.form['title']
    form_due = request.form['due']
    form_points = request.form['points']
    form_description = request.form['description']
    form_course = request.form['course']

    assignment = {}
    # if the user changed any of these, replace them in database
    if form_title:
        assignment["title"] = form_title
    else:
        assignment["title"] = title
    if form_description:
        assignment["description"] = form_description
    else:
        assignment["description"] = description
    if form_due:
        assignment["due"] = form_due
    else:
        assignment["due"] = due
    if form_points:
        assignment["points"] = form_points
    else:
        assignment["points"] = points

    assignment["course"] = form_course.strip()

    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    cursor.execute(f'''UPDATE assignment
                        SET title = %s,
                        description = %s,
                        due = %s,
                        points = %s,
                        course = %s
                        WHERE assignment_id = %s''',
                   (assignment['title'], assignment['description'],
                    assignment['due'], assignment['points'],
                    assignment['course'], assignment_id))

    db_conn.commit()
    cursor.close()
    db_pool.putconn(db_conn)
    return redirect(url_for('gradebook', course_id = assignment['course']))

### Delete Assignment
@app.route('/deleteAssigment/<assignment_id>/<course_id>', methods=['POST'])
def deleteAssignment(assignment_id, course_id):
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()
    sql = f'''DELETE FROM assignment WHERE assignment_id = {assignment_id};'''
    cursor.execute(sql)
    db_conn.commit()
    cursor.close()
    db_pool.putconn(db_conn)
    return redirect(url_for('gradebook', course_id=course_id))

@app.route('/addcourse/<teacher_id>', methods=['GET', 'POST'])
def addCourse(teacher_id):
    db_conn = db_pool.getconn()
    dict_cur = db_conn.cursor(cursor_factory=extras.DictCursor)

    addCourseForm = CourseForm()
    dict_cur.execute('SELECT teacher_id, first_name, last_name FROM teacher')
    choices = [(row['teacher_id'], '{} {}'.format(row['first_name'], row['last_name'])) for row in dict_cur]
    choices.append(('', 'NULL'))
    addCourseForm.teacher.choices = choices

    dict_cur.close()
    db_pool.putconn(db_conn)

    return render_template('addcourse.html', addCourseForm=addCourseForm, teacher_id=teacher_id)

@app.route('/courses', methods=['GET', 'POST'])
@app.route('/courses/<department>', methods=['GET', 'POST'])
def renderCourses(department="All"):
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()
    cursor.execute(f"SELECT department FROM course;")
    rows = cursor.fetchall()
    departments = list(set([row[0].strip() for row in rows]))
    if department == 'All':
        cursor.execute(f"SELECT * FROM course;")
    else:
        cursor.execute(f"SELECT * FROM course WHERE department = '{department}';")
    courselist = cursor.fetchall()
    courses = []

    for course in courselist:
        course = {'course_id': course[0], 'title': course[1].strip(), 'section': course[2], 'department': course[3].strip(), 'description': course[4], 'units': course[5] }
        courses.append(course)
    cursor.close()
    db_pool.putconn(db_conn)
    return render_template('courses.html', courses=courses, departments=departments)

@app.route('/saveaddcourse/<teacher_id>', methods=['POST'])
def saveAddCourse(teacher_id):

    title = request.form['title']
    section = request.form['section']
    department = request.form['department']
    description = request.form['description']
    units = request.form['units']
    teacher = teacher_id

    newcourse = {
        "title": title,
        "section": section,
        "department": department,
        "description": description,
        "units": units,
        "teacher": teacher
        }

    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()
    sql = f'''INSERT INTO course
    (title, section, department, description, units, teacher)
    VALUES (%s, %s, %s, %s, %s, %s);'''
    cursor.execute(sql,
                (newcourse['title'],
                 str(newcourse["section"]),
                 newcourse["department"],
                 newcourse["description"],
                 str(newcourse["units"]),
                 newcourse["teacher"]
                ))
    db_conn.commit()
    cursor.close()
    db_pool.putconn(db_conn)
    return redirect(url_for('editTeacher', teacher_id=teacher))

### Edit Course Form
@app.route('/editcourse/<course_id>', methods=['GET', 'POST'])
def editCourse(course_id):
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    cursor.execute(f"SELECT * "
                   f"FROM course "
                   f"INNER JOIN teacher on course.teacher = teacher.teacher_id "
                   f"INNER JOIN student_course on course.course_id = student_course.course_id "
                   f"INNER JOIN student on student_course.student_id = student.student_id "
                   f"WHERE course.course_id = {course_id}")

    results = cursor.fetchall()
    if len(results):
        result = results[0]
        course = {
            'course_id': result[0],
            'title': result[1].strip(),
            'section': result[2],
            'department': result[3],
            'description': result[4],
            'units': result[5],
            'teacher': result[6],
            'teachername': result[8].strip() + ' ' + result[9].strip()
            }

        students = [{'student_id': result[14], 'student_name': result[15].strip() + ' ' + result[16].strip()} for result in results]
        course['students'] = students
    else:
        cursor.execute(f"SELECT * FROM course WHERE course_id={course_id};")
        course = cursor.fetchall()[0]
        course = {
            'course_id': course[0],
            'title': course[1].strip(),
            'section': course[2],
            'department': course[3],
            'description': course[4],
            'units': course[5],
            'teacher': course[6]
        }

    # set the teacher dropdown
    editCourseForm = CourseForm()
    # cursor.execute('SELECT teacher_id, first_name, last_name FROM teacher;')
    # choices = [(row[0], '{} {}'.format(row[1], row[2])) for row in cursor]
    # choices.append(('', 'NULL'))
    # editCourseForm.teacher.choices = choices
    # cursor.execute('SELECT teacher FROM course WHERE course_id= %s', course_id)
    # editCourseForm.teacher.default = cursor.fetchone()[0] or ''
    # editCourseForm.process()

    cursor.close()
    db_pool.putconn(db_conn)

    return render_template('editcourse.html', editCourseForm=editCourseForm, course=course)

### Save Course Edits
@app.route('/saveEditCourse/<title>/<section>/<department>/<description>/<units>/<course_id>', methods=['POST'])
def saveEditCourse(title, section, department, description, units, course_id):

    form_title = request.form['title']
    form_section = request.form['section']
    form_department = request.form['department']
    form_description = request.form['description']
    form_units = request.form['units']
    form_teacher = request.form['teacher']

    course = {}
    # if the user changed any of these, replace them in database
    if form_title:
        course["title"] = form_title
    else:
        course["title"] = title
    if form_section:
        course["section"] = form_section
    else:
        course["section"] = section
    if form_department:
        course["department"] = form_department
    else:
        course["department"] = department
    if form_description :
        course["description"] = form_description
    else:
        course["description"] = description
    if form_units:
        course["units"] = form_units
    else:
        course["units"] = units

    course['teacher'] = form_teacher

    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()
    sql = f'''UPDATE course SET title = %s, section = %s, department = %s, description = %s, units = %s, teacher = %s WHERE course_id = %s;'''
    cursor.execute(sql,
                (course['title'],
                 course['section'],
                 course["department"],
                 course["description"],
                 course["units"],
                 course['teacher'],
                 course_id))
    db_conn.commit()
    cursor.close()
    db_pool.putconn(db_conn)
    # return redirect(url_for('renderCourses')) #
    return redirect(url_for('editTeacher', teacher_id=course["teacher"]))

### Delete Course
@app.route('/deleteCourse/<course_id>', methods=['POST'])
def deleteCourse(course_id):
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()
    sql = f'''DELETE FROM course WHERE course_id = {course_id};'''
    cursor.execute(sql)
    db_conn.commit()
    cursor.close()
    db_pool.putconn(db_conn)
    return redirect(url_for('renderCourses'))


@app.route('/addteacher', methods=['GET', 'POST'])
def addTeacher():
    addTeacherForm = TeacherForm()
    return render_template('addteacher.html', addTeacherForm=addTeacherForm)

@app.route('/', methods=['GET', 'POST'])
@app.route('/<department>', methods=['GET', 'POST'])
def renderTeachers(department='All'):
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()
    cursor.execute(f"SELECT department FROM course;")
    rows = cursor.fetchall()
    departments = list(set([row[0].strip() for row in rows]))

    if department == 'All':
        cursor.execute("SELECT DISTINCT teacher_id, first_name, last_name, email, telephone, course.department FROM teacher "
                       f"LEFT OUTER JOIN course on teacher.teacher_id = course.teacher ;")
    else:
        cursor.execute(f"SELECT DISTINCT teacher_id, first_name, last_name, email, telephone, course.department FROM teacher "
                       f"LEFT OUTER JOIN course on teacher.teacher_id = course.teacher "
                       f" WHERE course.department = '{department}';"
                        )
    teacherlist = cursor.fetchall()

    teachers = []
    for teacher in teacherlist:
        if teacher[5]:
            dept = teacher[5].strip()
        else:
            dept = None
        teachers.append(
            {'teacher_id': teacher[0], 'first_name': teacher[1].strip(), 'last_name': teacher[2].strip(),
             'email': teacher[3].strip(), 'telephone': teacher[4], 'dept': dept})

    cursor.close()
    db_pool.putconn(db_conn)
    return render_template('teachers.html', teachers=teachers, departments=departments)

@app.route('/saveAddTeacher', methods=['POST'])
def saveAddTeacher():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    telephone = request.form['telephone']
    email = request.form['email']

    newteacher = {"first_name": first_name, "last_name": last_name, "email": email, "telephone": telephone}

    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()
    sql = f'''INSERT INTO teacher
    (first_name, last_name, email, telephone)
    VALUES (%s, %s, %s, %s);'''
    cursor.execute(sql,
                (newteacher['first_name'],
                 newteacher["last_name"],
                 newteacher["email"],
                 newteacher["telephone"]))
    db_conn.commit()
    cursor.close()
    db_pool.putconn(db_conn)
    return redirect(url_for('renderTeachers'))

@app.route('/editTeacher/<teacher_id>', methods=['GET', 'POST'])
def editTeacher(teacher_id):
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()
    cursor.execute(f"SELECT * FROM teacher WHERE teacher_id={teacher_id};")
    cursor.execute(f"SELECT * "
                   f"FROM teacher "
                   f"INNER JOIN course on teacher.teacher_id = course.teacher "
                   f"WHERE teacher.teacher_id = {teacher_id}")

    results = cursor.fetchall()
    if len(results):
        teacher = results[0]
        teacher = {'teacher_id': teacher[0], 'first_name': teacher[1].strip(), 'last_name': teacher[2].strip(), 'email': teacher[3], 'telephone': teacher[4]}
        courses = [{'course_id': result[5], 'coursename': result[6].strip(), 'department': result[8].strip()} for result in results]
        teacher['courses'] = courses
    else:
        cursor.execute(f"SELECT * FROM teacher WHERE teacher_id={teacher_id};")
        teacher = cursor.fetchall()[0]
        teacher = {'teacher_id': teacher[0], 'first_name': teacher[1].strip(), 'last_name': teacher[2].strip(),
                   'email': teacher[3], 'telephone': teacher[4]}
    cursor.close()
    db_pool.putconn(db_conn)
    editTeacherForm = TeacherForm()
    return render_template('editteacher.html', editTeacherForm=editTeacherForm, teacher=teacher)

@app.route('/saveEditTeacher/<first_name>/<last_name>/<email>/<telephone>/<teacher_id>', methods=['POST'])
def saveEditTeacher(first_name, last_name, email, telephone, teacher_id):
    form = TeacherForm(request.form)
    teacher = {}
    if request.method == 'POST' and form.validate():
        teacher["first_name"] = request.form['first_name']
        teacher["last_name"] = request.form['last_name']
        teacher["email"] = request.form['email']
        teacher["telephone"] = request.form['telephone']
        if teacher["telephone"] == "0":
            teacher["telephone"] = ""
        print(teacher)
        db_conn = db_pool.getconn()
        cursor = db_conn.cursor()
        sql = f'''UPDATE teacher SET first_name = %s, last_name = %s, email = %s, telephone = %s WHERE teacher_id = %s;'''
        cursor.execute(sql,
                    (teacher['first_name'],
                     teacher['last_name'],
                     teacher['email'],
                     teacher['telephone'],
                     teacher_id))

        db_conn.commit()
        cursor.close()
        db_pool.putconn(db_conn)

    return redirect(url_for('renderTeachers'))

# @app.route('/saveEditTeacher/<first_name>/<last_name>/<email>/<telephone>/<teacher_id>', methods=['POST'])
# def saveEditTeacher(first_name, last_name, email, telephone, teacher_id):
#     form_first_name, form_last_name, form_email, form_telephone = None, None, None, None
#     form = TeacherForm(request.form)
#     if request.method == 'POST' and form.validate():
#         form_first_name = request.form['first_name']
#         form_last_name = request.form['last_name']
#         form_email = request.form['email']
#         form_telephone = request.form['telephone']
#     teacher = {}
#     # if the user changed any of these, replace them in database
#     if form_first_name:
#         teacher["first_name"] = form_first_name
#     else:
#         teacher["first_name"] = first_name
#     if form_last_name:
#         teacher["last_name"] = form_last_name
#     else:
#         teacher["last_name"] = last_name
#     if form_email:
#         teacher["email"] = form_email
#     else:
#         teacher["email"] =email
#     if form_telephone:
#         if form_telephone == "0":
#             teacher["telephone"] = ""
#         else:
#             teacher["telephone"] = form_telephone
#     else:
#         teacher["telephone"] = telephone
#
#     db_conn = db_pool.getconn()
#     cursor = db_conn.cursor()
#     sql = f'''UPDATE teacher SET first_name = %s, last_name = %s, email = %s, telephone = %s WHERE teacher_id = %s;'''
#     cursor.execute(sql,
#                 (teacher['first_name'],
#                  teacher['last_name'],
#                  teacher['email'],
#                  teacher['telephone'],
#                  teacher_id))
#
#     db_conn.commit()
#     cursor.close()
#     db_pool.putconn(db_conn)
#
#     return redirect(url_for('renderTeachers'))

@app.route('/deleteTeacher/<teacher_id>', methods=['POST'])
def deleteTeacher(teacher_id):
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()
    sql = f'''DELETE FROM teacher WHERE teacher_id = {teacher_id};'''
    cursor.execute(sql)
    db_conn.commit()
    cursor.close()
    db_pool.putconn(db_conn)

    return redirect(url_for('renderTeachers'))


### View all submissions for all courses
@app.route('/submissions', methods=['GET'])
def viewsubmissions():
    db_conn = db_pool.getconn()
    dict_cur = db_conn.cursor(cursor_factory=extras.DictCursor)
    dict_cur.execute('''
        SELECT student.student_id, submission.submission_id, first_name, last_name, grade, submitted, assignment
        FROM submission
        INNER JOIN student_submission ON student_submission.submission_id = submission.submission_id
        INNER JOIN student ON student.student_id = student_submission.student_id
        ORDER BY last_name ASC;
        ''')
    submissions = dict_cur.fetchall()

    dict_cur.close()
    db_pool.putconn(db_conn)
    return render_template('viewsubmissions.html', submissions=submissions)


### Add new submission
@app.route('/addsubmission', methods=['GET', 'POST'])
def addsubmission():
    if request.method == 'GET':
        db_conn = db_pool.getconn()
        dict_cur = db_conn.cursor(cursor_factory=extras.DictCursor)

        # assign choices to the form
        form = SubmissionForm()
        dict_cur.execute('SELECT assignment_id, title FROM assignment;')
        choices = [(row['assignment_id'], row['title']) for row in dict_cur]
        choices.append(('', 'NULL'))
        form.assignment.choices = choices

        dict_cur.execute('SELECT student_id, first_name, last_name FROM student;')
        form.students.choices = [(row['student_id'], '{} {}'.format(row['first_name'], row['last_name'])) for row in dict_cur]

        dict_cur.close()
        db_pool.putconn(db_conn)

        return render_template('addsubmission.html', submission_form=form)
    else:
        db_conn = db_pool.getconn()
        cursor = db_conn.cursor()

        # insert new submission
        assignment_input = request.form['assignment'] or None
        sql_string = 'INSERT INTO submission (submitted, grade, assignment) VALUES (%s, %s, %s) RETURNING submission_id'
        cursor.execute(sql_string, (request.form['sub_time'], request.form['grade'], assignment_input))
        last_id = cursor.fetchone()[0]

        # add submission's student relations
        student_ids = request.form.getlist('students')
        values = [(student_id, str(last_id)) for student_id in student_ids]
        sql_string = 'INSERT INTO student_submission (student_id, submission_id) VALUES %s'
        extras.execute_values(cursor, sql_string, values)

        db_conn.commit()
        cursor.close()
        db_pool.putconn(db_conn)
        return redirect(url_for('viewsubmissions'))


### Login route
@app.route('/login/<id>', methods=['GET'])
def login(id):
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    cursor.execute('SELECT teacher_id, first_name, last_name FROM teacher WHERE teacher_id = %s', id)
    row = cursor.fetchone()
    if not row:
        abort(404, 'No teacher found for id')

    session['user'] = {'id': row[0], 'name': '{} {}'.format(row[1], row[2])}

    cursor.close()
    db_pool.putconn(db_conn)

    return redirect(url_for('renderTeachers'))

### Admin page
@app.route('/admin', methods=['GET'])
@app.route('/admin/<table>', methods=['GET', 'POST'])
def viewadmin(table=None):
    result = urlparse(app.config['DATABASE_URL'])

    db_conn = db_pool.getconn()

    if not table:
        cur = db_conn.cursor()
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE (table_schema = 'public')
            """)
        table_names = [name[0] for name in cur.fetchall()]
        cur.close()
        db_pool.putconn(db_conn)

        return render_template('admin.html', table_names=table_names)

    if request.method == 'GET':
        cur = db_conn.cursor()
        cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE (table_schema = 'public')
            """)
        table_names = [name[0] for name in cur.fetchall()]
        cur.close()

        dict_cur = db_conn.cursor(cursor_factory=extras.DictCursor)
        dict_cur.execute('SELECT * FROM {};'.format(table))
        columns = [desc[0] for desc in dict_cur.description]
        records = dict_cur.fetchall()
        dict_cur.close()

        db_pool.putconn(db_conn)

        return render_template('admin.html', table=records, columns=columns, table_names=table_names, title=table)
    else:
        values = [v if v != '' else None for v in request.form.values()]

        cur = db_conn.cursor()
        cur.execute(
            sql.SQL('INSERT INTO {} VALUES ({})').format(
                sql.Identifier(table),
                sql.SQL(', ').join(sql.Placeholder() * len(values))
            ),
            values
        )
        db_conn.commit()
        cur.close()

        db_pool.putconn(db_conn)

        return redirect('/admin/{}'.format(table))

