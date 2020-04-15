from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import ClassesForm, StudentForm, AssignmentForm, AddCourseForm
from psycopg2 import connect, extensions, sql
from urllib.parse import urlparse

# initialize students and arrays
students = []
# eventually we will get these via SQL queries instead
dummystudent1 = Student('John', 'Doe', 'doe@gmail.com')
dummystudent2 = Student('Kanye', 'West', 'west@gmail.com')
students.append(dummystudent1)
students.append(dummystudent2)

assignments = []
# eventually we will get these via SQL queries instead
dummyassignment1 = Assignment('HW 1', '01-01-2020', 5)
dummyassignment2 = Assignment('HW 2', '01-02-2020', 10)
assignments.append(dummyassignment1)
assignments.append(dummyassignment2)

courses = []
# eventually we will get these via SQL queries instead
dummycourse1 = Course('Trig')
dummycourse2 = Course('Basket Weaving')
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
    print(getStudents('doe@gmail.com')) # delete later - just database example
    return render_template("about.html")

### Get classes via SQL query
def getClasses(teacherstring):
    con = sqlite3.connect("grades.db")
    teacher = "SELECT * FROM grades WHERE teacher=:teacher"
    cursor = con.execute(teacher, {"teacher": teacherstring})
    rows = cursor.fetchall()
    con.close()
    return rows

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

    newstudent = Student(first, last, email) 
    students.append(newstudent)      

    return redirect(url_for('index'))


### Edit Student Form
@app.route('/editstudent/<first>/<last>/<email>', methods=['GET', 'POST'])
def editStudent(first, last, email):
    # replace this for loop with database query eventually to find unique studentID
    for i, student in enumerate(students):
        if student.email == email:
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
        students[studentID].first = first
    if last:
        students[studentID].last = last
    if email:
        students[studentID].email = email        

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

    newassignment = Assignment(name, date, points) 
    assignments.append(newassignment)      

    return redirect(url_for('index'))


### Edit Assignment Form
@app.route('/editassignment/<name>/<date>/<points>', methods=['GET', 'POST'])
def editAssignment(name, date, points):
    # replace this for loop with database query eventually to find unique assignmentID
    for i, assignment in enumerate(assignments):
        if assignment.name == name:
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
        assignments[assignmentID].name = name
    if date:
        assignments[assignmentID].date = date
    if points:
        assignments[assignmentID].points = points     

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
    newcourse = Course(name)
    courses.append(newcourse)    
    return redirect(url_for('renderCourses'))

### Edit Course Form
@app.route('/editcourse/<courseName>', methods=['GET', 'POST'])
def editCourse(courseName):
    # replace this for loop with database query eventually to find unique courseID
    for i, course in enumerate(courses):
        if course.courseName == courseName:
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
        courses[courseID].courseName = courseName 

    return redirect(url_for('renderCourses'))

### Delete Course
@app.route('/deleteCourse/<courseID>', methods=['POST'])
def deleteCourse(courseID):

    courseID = int(courseID)
    del courses[courseID]

    return redirect(url_for('renderCourses'))

@app.route('/testsql')
def testsql():

#    result = urlparse("postgresql://objectrocket:mypass@localhost/postgres")
    result = urlparse("postgres://dnksgzdceixveu:e9289a3cd88b80874ba424a0e5f14c20113572f675cedc70a4cb5b94ba875c3a@ec2-18-206-84-251.compute-1.amazonaws.com:5432/dq7nmi44nhj5q")
    # also in python 3+ use: urlparse("YourUrl") not urlparse.urlparse("YourUrl") 
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