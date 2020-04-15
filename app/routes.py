from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import ClassesForm, StudentForm, AssignmentForm, AddCourseForm
from psycopg2 import connect, extensions, sql
from urllib.parse import urlparse

# initialize students and arrays
students = []
# eventually we will get these via SQL queries instead
dummystudent1 = {"first": "John", "last": "Doe", "email": "doe@gmail.com"}
dummystudent2 = {"first": "Kanye", "last": "West", "email": "kanye@gmail.com"}
students.append(dummystudent1)
students.append(dummystudent2)

assignments = []
# eventually we will get these via SQL queries instead
dummyassignment1 = {"name": "HW 1 ", "date": "01-01-2020", "points": "10"}
dummyassignment2 = {"name": "HW 2 ", "date": "01-02-2020", "points": "5"}
assignments.append(dummyassignment1)
assignments.append(dummyassignment2)

courses = []
# eventually we will get these via SQL queries instead
dummycourse1 = {"courseName": "Trig"}
dummycourse2 = {"courseName": "Basket Weaving"}
courses.append(dummycourse1)
courses.append(dummycourse2)

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

    newstudent = {"first": first, "last": last, "email": email}
    students.append(newstudent)      

    return redirect(url_for('index'))


### Edit Student Form
@app.route('/editstudent/<first>/<last>/<email>', methods=['GET', 'POST'])
def editStudent(first, last, email):
    # replace this for loop with database query eventually to find unique studentID
    for i, student in enumerate(students):
        if student["email"] == email:
            studentID = i

    editStudentForm = StudentForm()
    return render_template('editstudent.html', editStudentForm=editStudentForm, first=first, last=last, email=email, studentID = studentID)

### Save Student Edits
@app.route('/saveEditStudent/<studentID>', methods=['POST'])
def saveEditStudent(studentID):

    studentID = int(studentID)
    first = request.form['first']
    last = request.form['last']
    email = request.form['email']

    # if the user changed any of these, replace them in database
    if first:
        students[studentID]["first"] = first
    if last:
        students[studentID]["last"] = last
    if email:
        students[studentID]["email"] = email        

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

    name = request.form['name']
    date = request.form['date']
    points = request.form['points']

    newassignment = {"name": name, "date": date, "points": points} 
    assignments.append(newassignment)      

    return redirect(url_for('index'))


### Edit Assignment Form
@app.route('/editassignment/<name>/<date>/<points>', methods=['GET', 'POST'])
def editAssignment(name, date, points):
    # replace this for loop with database query eventually to find unique assignmentID
    for i, assignment in enumerate(assignments):
        if assignment["name"] == name:
            assignmentID = i

    editAssignmentForm = AssignmentForm()
    return render_template('editassignment.html', editAssignmentForm=editAssignmentForm, name=name, date=date, points=points, assignmentID=assignmentID)

### Save Assignment Edits
@app.route('/saveEditAssignment/<assignmentID>', methods=['POST'])
def saveEditAssignment(assignmentID):

    assignmentID = int(assignmentID)
    name = request.form['name']
    date = request.form['date']
    points = request.form['points']

    # if the user changed any of these, replace them in database
    if name:
        assignments[assignmentID]["name"] = name
    if date:
        assignments[assignmentID]["date"] = date
    if points:
        assignments[assignmentID]["points"] = points     

    return redirect(url_for('index'))

### Delete Assignment
@app.route('/deleteAssigment/<assignmentID>', methods=['POST'])
def deleteAssignment(assignmentID):

    assignmentID = int(assignmentID)
    del assignments[assignmentID]

    return redirect(url_for('index'))

@app.route('/addcourse', methods=['GET', 'POST'])
def addCourse():
    addCourseForm = AddCourseForm()
    return render_template('addcourse.html', addCourseForm=addCourseForm)

@app.route('/courses', methods=['GET', 'POST'])
def renderCourses():
    return render_template('courses.html', courses=courses)

@app.route('/saveAddCourse', methods=['POST'])
def saveAddCourse():

    name = request.form['courseName']
    newcourse = {"courseName": name}
    courses.append(newcourse)    
    return redirect(url_for('renderCourses'))

### Edit Course Form
@app.route('/editcourse/<courseName>', methods=['GET', 'POST'])
def editCourse(courseName):
    # replace this for loop with database query eventually to find unique courseID
    for i, course in enumerate(courses):
        if course["courseName"] == courseName:
            courseID = i

    editCourseForm = AddCourseForm()
    return render_template('editcourse.html', editCourseForm=editCourseForm, courseName=courseName, courseID=courseID)

### Save Course Edits
@app.route('/saveEditCourse/<courseID>', methods=['POST'])
def saveEditCourse(courseID):

    courseID = int(courseID)
    courseName = request.form['courseName']

    # if the user changed any of these, replace them in database
    if courseName:
        courses[courseID]["courseName"] = courseName 

    return redirect(url_for('renderCourses'))

### Delete Course
@app.route('/deleteCourse/<courseID>', methods=['POST'])
def deleteCourse(courseID):

    courseID = int(courseID)
    del courses[courseID]

    return redirect(url_for('renderCourses'))


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