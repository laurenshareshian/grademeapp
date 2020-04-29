from flask import render_template, flash, redirect, url_for, request, g
from app import app
from app.forms import TeacherForm, StudentForm, AssignmentForm, CourseForm, SubmissionForm
from psycopg2 import connect, extensions, sql, extras
from urllib.parse import urlparse

result = urlparse(app.config['DATABASE_URL'])

username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname
port = result.port
print(username, password, database, hostname, port)
conn = connect(
    database=database,
    user=username,
    password=password,
    host=hostname,
    port=port
)
cursor = conn.cursor()


@app.route('/')
#@app.route('/index')
def index():
    cursor.execute("SELECT * FROM student;")
    studentlist = cursor.fetchall()
    students = []
    for student in studentlist:
        students.append({'student_id': student[0], 'first_name': student[1].strip(), 'last_name': student[2].strip(), 'year': student[3], 'email': student[4].strip(), 'telephone': student[5] })

    cursor.execute("SELECT * FROM assignment;")
    assignmentlist = cursor.fetchall()
    assignments = []
    for assignment in assignmentlist:
        assignments.append({'assignment_id': assignment[0], 'title': assignment[1].strip(), 'description': assignment[2].strip(), 'due': assignment[3], 'points': assignment[4] })

    addStudentForm = StudentForm()
    addAssignmentForm = AssignmentForm()
    return render_template('gradebook.html', addStudentForm=addStudentForm, addAssignmentForm=addAssignmentForm, students=students, assignments=assignments)

### About Tab
@app.route("/about")
def about():
    return render_template("about.html")

### Add New Student Form
@app.route('/addstudent', methods=['GET', 'POST'])
def addStudent():

    addStudentForm = StudentForm()
    return render_template('addstudent.html', addStudentForm=addStudentForm)

### Save Add Student
@app.route('/saveAddStudent', methods=['POST'])
def saveAddStudent():

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    telephone = request.form['telephone']
    year = request.form['year']

    newstudent = {"first_name": first_name, "last_name": last_name, "email": email, "telephone": telephone, "year": year}

    cursor = conn.cursor()
    sql = f'''INSERT INTO student 
    (first_name, last_name, email, telephone, year) 
    VALUES (%s, %s, %s, %s, %s);'''
    cursor.execute(sql,
                (newstudent['first_name'],
                 newstudent["last_name"],
                 newstudent["email"],
                 newstudent["telephone"],
                 newstudent["year"]))
    conn.commit()

    return redirect(url_for('index'))


### Edit Student Form
@app.route('/editstudent/<student_id>', methods=['GET', 'POST'])
def editStudent(student_id):
    cursor.execute(f"SELECT * FROM student WHERE student_id={student_id};")
    student = cursor.fetchall()[0]
    student = {'student_id': student[0], 'first_name': student[1].strip(), 'last_name': student[2].strip(), 'year': student[3], 'email': student[4].strip(), 'telephone': student[5] }

    editStudentForm = StudentForm()
    return render_template('editstudent.html', editStudentForm=editStudentForm, student=student)

### Save Student Edits
@app.route('/saveEditStudent/<first_name>/<last_name>/<year>/<email>/<telephone>/<student_id>', methods=['POST'])
def saveEditStudent(first_name, last_name, year, email, telephone, student_id):

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
        student["telephone"] = form_telephone
    else:
        student["telephone"] = telephone

    sql = f'''UPDATE student SET first_name = %s, last_name = %s, year = %s, email = %s, telephone = %s WHERE student_id = %s;'''
    cursor.execute(sql,
                (student['first_name'],
                 student['last_name'],
                 str(student['year']),
                 student['email'],
                 str(student['telephone']),
                 str(student_id)))
    conn.commit()
    return redirect(url_for('index'))

### Delete Student
@app.route('/deleteStudent/<student_id>', methods=['POST'])
def deleteStudent(student_id):

    sql = f'''DELETE FROM student WHERE student_id={student_id};'''
    cursor.execute(sql)
    conn.commit()

    return redirect(url_for('index'))

### Add New Assignment Form
@app.route('/addassignment', methods=['GET', 'POST'])
def addAssignment():

    addAssignmentForm = AssignmentForm()
    return render_template('addassignment.html', addAssignmentForm=addAssignmentForm)

### Save Add Assignment
@app.route('/saveAddAssignment', methods=['POST'])
def saveAddAssignment():

    title = request.form['title']
    due = request.form['due']
    points = request.form['points']
    description = request.form['description']

    newassignment = {"title": title, "due": due, "points": points, "description": description}

    cursor = conn.cursor()
    sql = f'''INSERT INTO assignment
    (title, due, points, description) 
    VALUES (%s, %s, %s, %s);'''
    cursor.execute(sql,
                (newassignment['title'],
                 str(newassignment["due"]),
                 str(newassignment["points"]),
                 newassignment["description"]))
    conn.commit()

    return redirect(url_for('index'))

### Edit Assignment Form
@app.route('/editassignment/<assignment_id>', methods=['GET', 'POST'])
def editAssignment(assignment_id):

    cursor.execute(f"SELECT * FROM assignment WHERE assignment_id={assignment_id};")
    assignment = cursor.fetchall()[0]
    assignment = {'assignment_id': assignment[0], 'title': assignment[1].strip(), 'description': assignment[2].strip(), 'due': assignment[3], 'points': assignment[4]}
    print(assignment)
    editAssignmentForm = AssignmentForm()
    return render_template('editassignment.html', editAssignmentForm=editAssignmentForm, assignment=assignment)

### Save Assignment Edits
@app.route('/saveEditAssignment/<title>/<description>/<due>/<points>/<assignment_id>', methods=['POST'])
def saveEditAssignment(title, description, due, points, assignment_id):

    form_title = request.form['title']
    form_due = request.form['due']
    form_points = request.form['points']
    form_description = request.form['description']

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
        assignment["points"] = points
    else:
        assignment["points"] = points

    sql = f'''UPDATE assignment SET title = %s, description = %s, due = %s, points = %s WHERE assignment_id = %s;'''
    cursor.execute(sql,
                (assignment['title'],
                 assignment["description"],
                 str(assignment["due"]),
                 str(assignment["points"]),
                 str(assignment_id)))
    conn.commit()

    return redirect(url_for('index'))

### Delete Assignment
@app.route('/deleteAssigment/<assignment_id>', methods=['POST'])
def deleteAssignment(assignment_id):

    sql = f'''DELETE FROM assignment WHERE assignment_id = {assignment_id};'''
    cursor.execute(sql)
    conn.commit()
    return redirect(url_for('index'))

@app.route('/addcourse', methods=['GET', 'POST'])
def addCourse():
    addCourseForm = CourseForm()
    return render_template('addcourse.html', addCourseForm=addCourseForm)

@app.route('/courses', methods=['GET', 'POST'])
def renderCourses():
    cursor.execute("SELECT * FROM course;")
    courselist = cursor.fetchall()
    courses = []
    for course in courselist:
        courses.append({'course_id': course[0], 'title': course[1].strip(), 'section': course[2], 'department': course[3].strip(), 'description': course[4], 'units': course[5] })

    return render_template('courses.html', courses=courses)

@app.route('/saveAddCourse', methods=['POST'])
def saveAddCourse():

    title = request.form['title']
    section = request.form['section']
    department = request.form['department']
    description = request.form['description']
    units = request.form['units']
    newcourse = {"title": title, "section": section, "department": department, "description": description, "units": units}

    cursor = conn.cursor()
    sql = f'''INSERT INTO course
    (title, section, department, description, units) 
    VALUES (%s, %s, %s, %s, %s);'''
    cursor.execute(sql,
                (newcourse['title'],
                 str(newcourse["section"]),
                 newcourse["department"],
                 newcourse["description"],
                 str(newcourse["units"])))
    conn.commit()

    return redirect(url_for('renderCourses'))

### Edit Course Form
@app.route('/editcourse/<course_id>', methods=['GET', 'POST'])
def editCourse(course_id):
    cursor.execute(f"SELECT * FROM course WHERE course_id={course_id};")
    course = cursor.fetchall()[0]
    course = {'course_id': course[0], 'title': course[1].strip(), 'section': course[2], 'department': course[3], 'description': course[4], 'units': course[5]}
    editCourseForm = CourseForm()
    return render_template('editcourse.html', editCourseForm=editCourseForm, course=course)

### Save Course Edits
@app.route('/saveEditCourse/<title>/<section>/<department>/<description>/<units>/<course_id>', methods=['POST'])
def saveEditCourse(title, section, department, description, units, course_id):

    form_title = request.form['title']
    form_section = request.form['section']
    form_department = request.form['department']
    form_description = request.form['description']
    form_units = request.form['units']

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

    sql = f'''UPDATE course SET title = %s, section = %s, department = %s, description = %s, units = %s WHERE course_id = %s;'''
    cursor.execute(sql,
                (course['title'],
                 str(course['section']),
                 course["department"],
                 course["description"],
                 str(course["units"]),
                 str(course_id)))
    conn.commit()
    return redirect(url_for('renderCourses'))

### Delete Course
@app.route('/deleteCourse/<course_id>', methods=['POST'])
def deleteCourse(course_id):

    sql = f'''DELETE FROM course WHERE course_id = {course_id};'''
    cursor.execute(sql)
    conn.commit()
    return redirect(url_for('renderCourses'))


@app.route('/addteacher', methods=['GET', 'POST'])
def addTeacher():
    addTeacherForm = TeacherForm()
    return render_template('addteacher.html', addTeacherForm=addTeacherForm)

@app.route('/teachers', methods=['GET', 'POST'])
def renderTeachers():
    cursor.execute("SELECT * FROM teacher;")
    teacherlist = cursor.fetchall()
    teachers = []
    for teacher in teacherlist:
        teachers.append({'teacher_id': teacher[0], 'first_name': teacher[1].strip(), 'last_name': teacher[2].strip(), 'email': teacher[3].strip(), 'telephone': teacher[4] })

    return render_template('teachers.html', teachers=teachers)

@app.route('/saveAddTeacher', methods=['POST'])
def saveAddTeacher():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    telephone = request.form['telephone']
    email = request.form['email']

    newteacher = {"first_name": first_name, "last_name": last_name, "email": email, "telephone": telephone}

    cursor = conn.cursor()
    sql = f'''INSERT INTO teacher
    (first_name, last_name, email, telephone) 
    VALUES (%s, %s, %s, %s);'''
    cursor.execute(sql,
                (newteacher['first_name'],
                 newteacher["last_name"],
                 newteacher["email"],
                 newteacher["telephone"]))
    conn.commit()
    return redirect(url_for('renderTeachers'))

@app.route('/editTeacher/<teacher_id>', methods=['GET', 'POST'])
def editTeacher(teacher_id):
    print('hereeeee')
    cursor.execute(f"SELECT * FROM teacher WHERE teacher_id={teacher_id};")
    teacher = cursor.fetchall()[0]
    teacher = {'teacher_id': teacher[0], 'first_name': teacher[1].strip(), 'last_name': teacher[2].strip(), 'email': teacher[3], 'telephone': teacher[4]}
    editTeacherForm = TeacherForm()
    return render_template('editteacher.html', editTeacherForm=editTeacherForm, teacher=teacher)

@app.route('/saveEditTeacher/<first_name>/<last_name>/<email>/<telephone>/<teacher_id>', methods=['POST'])
def saveEditTeacher(first_name, last_name, email, telephone, teacher_id):

    form_first_name = request.form['first_name']
    form_last_name = request.form['last_name']
    form_email = request.form['email']
    form_telephone = request.form['telephone']
    # if the user changed any of these, replace them in database
    teacher = {}
    # if the user changed any of these, replace them in database
    if form_first_name:
        teacher["first_name"] = form_first_name
    else:
        teacher["first_name"] = first_name
    if form_last_name:
        teacher["last_name"] = form_last_name
    else:
        teacher["last_name"] = last_name
    if form_email:
        teacher["email"] = form_email
    else:
        teacher["email"] =email
    if form_telephone:
        teacher["telephone"] = form_telephone
    else:
        teacher["telephone"] = telephone

    sql = f'''UPDATE teacher SET first_name = %s, last_name = %s, email = %s, telephone = %s WHERE teacher_id = %s;'''
    cursor.execute(sql,
                (teacher['first_name'],
                 teacher['last_name'],
                 teacher['email'],
                 teacher['telephone'],
                 str(teacher_id)))
    conn.commit()


    return redirect(url_for('renderTeachers'))

@app.route('/deleteTeacher/<teacher_id>', methods=['POST'])
def deleteTeacher(teacher_id):

    sql = f'''DELETE FROM teacher WHERE teacher_id = {teacher_id};'''
    cursor.execute(sql)
    conn.commit()

    return redirect(url_for('renderTeachers'))


### View all submissions for all courses
@app.route('/submissions', methods=['GET'])
def viewsubmissions():

    dict_cur = conn.cursor(cursor_factory=extras.DictCursor)
    dict_cur.execute('SELECT submission_id, submitted, grade FROM submission;')
    submissions = dict_cur.fetchall()

    return render_template('viewsubmissions.html', submissions=submissions)


### Add new submission
@app.route('/addsubmission', methods=['GET', 'POST'])
def addsubmission():
    if request.method == 'GET':
        return render_template('addsubmission.html', submission_form=SubmissionForm())
    else:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO submission (submitted, grade) 
            VALUES (%s, %s);
            ''',
            (request.form['sub_time'], request.form['grade']))
        return redirect(url_for('viewsubmissions'))


### This is a test that the postgres sql database is working
@app.route('/testsql')
def testsql():
    result = urlparse(app.config['DATABASE_URL'])
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port
    print(username, password, database, hostname, port)
    conn = connect(
        database = database,
        user = username,
        password = password,
        host = hostname,
        port = port
)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM student;")
    students = cursor.fetchall()
    print(students)

    cursor.execute("SELECT * FROM teacher;")
    teachers = cursor.fetchall()
    print(teachers)

    cursor.execute("SELECT * FROM course;")
    courses = cursor.fetchall()
    print(courses)

    cursor.execute("SELECT * FROM assignment;")
    assignments = cursor.fetchall()
    print(assignments)

    return render_template('testsql.html', students=students, teachers=teachers, courses=courses, assignments=assignments )