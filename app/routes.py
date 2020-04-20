from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import TeacherForm, StudentForm, AssignmentForm, CourseForm
from psycopg2 import connect, extensions, sql
from urllib.parse import urlparse

# initialize students and arrays
students = []
# eventually we will get these via SQL queries instead
dummystudent1 = {"first": "John", "last": "Doe", "email": "doe@gmail.com", "phone": "555-5555", "year": "2020"}
dummystudent2 = {"first": "Kanye", "last": "West", "email": "kanye@gmail.com", "phone": "555-5555", "year": "2020"}
students.append(dummystudent1)
students.append(dummystudent2)

assignments = []
# eventually we will get these via SQL queries instead
dummyassignment1 = {"title": "HW 1 ", "due": "01-01-2020", "points": "10", "description": "exercises"}
dummyassignment2 = {"title": "HW 2 ", "due": "01-02-2020", "points": "5", "description": "essay"}
assignments.append(dummyassignment1)
assignments.append(dummyassignment2)

courses = []
# eventually we will get these via SQL queries instead
dummycourse1 = {"title": "Trig", "section": "100", "description": "intro", "department": "math", "units": 5}
dummycourse2 = {"title": "Basket Weaving", "section": "100", "description": "intro", "department": "art", "units": 5}
courses.append(dummycourse1)
courses.append(dummycourse2)

teachers = []
# eventually we will get these via SQL queries instead
dummyteacher1 = {"first": "Lauren", "last": "Shareshian", "email": "doe@gmail.com", "phone": "555-5555"}
dummyteacher2 = {"first": "Joshua", "last": "Cox","email": "doe@gmail.com", "phone": "555-5555"}
teachers.append(dummyteacher1)
teachers.append(dummyteacher2)

@app.route('/')
#@app.route('/index')
def index():
    addStudentForm = StudentForm()
    addAssignmentForm = AssignmentForm()
    return render_template('gradebook.html', addStudentForm=addStudentForm, addAssignmentForm=addAssignmentForm, students=students, assignments=assignments)

### About Tab
@app.route("/about")
def about():
    return render_template("about.html")

### Add New Student Form
@app.route('/addnewstudent', methods=['GET', 'POST'])
def addNewStudent():

    addStudentForm = StudentForm()
    return render_template('addnewstudent.html', addStudentForm=addStudentForm)

### Save Add Student
@app.route('/saveAddStudent', methods=['POST'])
def saveAddStudent():

    first = request.form['first']
    last = request.form['last']
    email = request.form['email']
    phone = request.form['phone']
    year = request.form['year']

    newstudent = {"first": first, "last": last, "email": email, "phone": phone, "year": year}
    students.append(newstudent)      

    return redirect(url_for('index'))


### Edit Student Form
@app.route('/editstudent/<first>/<last>/<email>/<phone>/<year>', methods=['GET', 'POST'])
def editStudent(first, last, email, phone, year):
    # replace this for loop with database query eventually to find unique studentID
    for i, student in enumerate(students):
        if student["email"] == email:
            studentID = i

    editStudentForm = StudentForm()
    return render_template('editstudent.html', editStudentForm=editStudentForm, first=first, last=last, email=email, phone=phone, year=year, studentID = studentID)

### Save Student Edits
@app.route('/saveEditStudent/<studentID>', methods=['POST'])
def saveEditStudent(studentID):

    studentID = int(studentID)
    first = request.form['first']
    last = request.form['last']
    email = request.form['email']
    phone = request.form['phone']
    year = request.form['year']

    # if the user changed any of these, replace them in database
    if first:
        students[studentID]["first"] = first
    if last:
        students[studentID]["last"] = last
    if email:
        students[studentID]["email"] = email
    if phone:
        students[studentID]["phone"] = phone
    if year:
        students[studentID]["year"] = year

    return redirect(url_for('index'))

### Delete Student
@app.route('/deleteStudent/<studentID>', methods=['POST'])
def deleteStudent(studentID):

    studentID = int(studentID)
    del students[studentID]

    return redirect(url_for('index'))

### Add New Assignment Form
@app.route('/addnewassignment', methods=['GET', 'POST'])
def addNewAssignment():

    addAssignmentForm = AssignmentForm()
    return render_template('addnewassignment.html', addAssignmentForm=addAssignmentForm)

### Save Add Assignment
@app.route('/saveAddAssignment', methods=['POST'])
def saveAddAssignment():

    title = request.form['title']
    due = request.form['due']
    points = request.form['points']
    description = request.form['description']

    newassignment = {"title": title, "due": due, "points": points, "description": description}
    assignments.append(newassignment)      

    return redirect(url_for('index'))


### Edit Assignment Form
@app.route('/editassignment/<title>/<due>/<points>/<description>', methods=['GET', 'POST'])
def editAssignment(title, due, points, description):
    # replace this for loop with database query eventually to find unique assignmentID
    for i, assignment in enumerate(assignments):
        if assignment["title"] == title:
            assignmentID = i

    editAssignmentForm = AssignmentForm()
    return render_template('editassignment.html', editAssignmentForm=editAssignmentForm, title=title, due=due, points=points, description=description, assignmentID=assignmentID)

### Save Assignment Edits
@app.route('/saveEditAssignment/<assignmentID>', methods=['POST'])
def saveEditAssignment(assignmentID):

    assignmentID = int(assignmentID)
    title = request.form['title']
    due = request.form['due']
    points = request.form['points']
    description = request.form['description']

    # if the user changed any of these, replace them in database
    if title:
        assignments[assignmentID]["title"] = title
    if due:
        assignments[assignmentID]["due"] = due
    if points:
        assignments[assignmentID]["points"] = points     
    if description:
        assignments[assignmentID]["description"] = description

    return redirect(url_for('index'))

### Delete Assignment
@app.route('/deleteAssigment/<assignmentID>', methods=['POST'])
def deleteAssignment(assignmentID):

    assignmentID = int(assignmentID)
    del assignments[assignmentID]

    return redirect(url_for('index'))

@app.route('/addcourse', methods=['GET', 'POST'])
def addCourse():
    addCourseForm = CourseForm()
    return render_template('addcourse.html', addCourseForm=addCourseForm)

@app.route('/courses', methods=['GET', 'POST'])
def renderCourses():
    return render_template('courses.html', courses=courses)

@app.route('/saveAddCourse', methods=['POST'])
def saveAddCourse():

    title = request.form['title']
    section = request.form['section']
    department = request.form['department']
    description = request.form['description']
    units = request.form['units']
    newcourse = {"title": title, "section": section, "department": department, "description": description, "units": units}
    courses.append(newcourse)    
    return redirect(url_for('renderCourses'))

### Edit Course Form
@app.route('/editcourse/<title>/<section>/<department>/<description>/<units>', methods=['GET', 'POST'])
def editCourse(title, section, department, description, units):
    # replace this for loop with database query eventually to find unique courseID
    for i, course in enumerate(courses):
        if course["title"] == title:
            courseID = i

    editCourseForm = CourseForm()
    return render_template('editcourse.html', editCourseForm=editCourseForm, title=title, section=section, department=department, description=description, units=units, courseID=courseID)

### Save Course Edits
@app.route('/saveEditCourse/<courseID>', methods=['POST'])
def saveEditCourse(courseID):

    courseID = int(courseID)
    title = request.form['title']
    section = request.form['section']
    department = request.form['department']
    description = request.form['description']
    units = request.form['units']

    # if the user changed any of these, replace them in database
    if title:
        courses[courseID]["title"] = title
    if section:
        courses[courseID]["section"] = section
    if department:
        courses[courseID]["department"] = department
    if description:
        courses[courseID]["description"] = description
    if units:
        courses[courseID]["units"] = units

    return redirect(url_for('renderCourses'))

### Delete Course
@app.route('/deleteCourse/<courseID>', methods=['POST'])
def deleteCourse(courseID):

    courseID = int(courseID)
    del courses[courseID]

    return redirect(url_for('renderCourses'))


@app.route('/addteacher', methods=['GET', 'POST'])
def addTeacher():
    addTeacherForm = TeacherForm()
    return render_template('addteacher.html', addTeacherForm=addTeacherForm)

@app.route('/teachers', methods=['GET', 'POST'])
def renderTeachers():
    return render_template('teachers.html', teachers=teachers)

@app.route('/saveAddTeacher', methods=['POST'])
def saveAddTeacher():
    first = request.form['first']
    last = request.form['last']
    phone = request.form['phone']
    email = request.form['email']

    newteacher = {"first": first, "last": last, "email": email, "phone": phone}
    teachers.append(newteacher)
    return redirect(url_for('renderTeachers'))

@app.route('/editteacher/<first>/<last>/<email>/<phone>', methods=['GET', 'POST'])
def editTeacher(first, last, email, phone):
    # replace this for loop with database query eventually to find unique courseID
    for i, teacher in enumerate(teachers):
        if teacher["first"] == first and teacher["last"] == last:
            teacherID = i

    editTeacherForm = TeacherForm()
    return render_template('editteacher.html', editTeacherForm=editTeacherForm, first=first, last=last, email=email, phone=phone, teacherID=teacherID)

@app.route('/saveEditTeacher/<teacherID>', methods=['POST'])
def saveEditTeacher(teacherID):

    teacherID = int(teacherID)
    first = request.form['first']
    last = request.form['last']
    email = request.form['email']
    phone = request.form['phone']
    # if the user changed any of these, replace them in database
    if first:
        teachers[teacherID]["first"] = first
    if last:
        teachers[teacherID]["last"] = last
    if email:
        teachers[teacherID]["email"] = email
    if phone:
        teachers[teacherID]["phone"] = phone
    return redirect(url_for('renderTeachers'))

@app.route('/deleteTeacher/<teacherID>', methods=['POST'])
def deleteTeacher(teacherID):

    teacherID = int(teacherID)
    del teachers[teacherID]

    return redirect(url_for('renderTeachers'))



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
    cursor.execute("SELECT * FROM students;")
    names = cursor.fetchall()
    print(names)
    return render_template('testsql.html', names=names)