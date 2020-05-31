from flask import render_template, redirect, url_for, \
    request, session, abort, g
from app import app
from app.forms import TeacherForm, StudentForm, \
    AssignmentForm, CourseForm, SubmissionForm
from psycopg2 import sql, extras
import numpy as np
from app.db import db_pool

app.secret_key = "cleverpassword"


def handle_login():
    """Handle user switching"""
    if 'user' not in session:
        db_conn = db_pool.getconn()
        cursor = db_conn.cursor()

        cursor.execute('SELECT teacher_id, first_name, last_name FROM teacher')
        row = cursor.fetchone()
        session['user'] = {
            'id': str(
                row[0]), 'name': '{} {}'.format(
                row[1], row[2])}

        cursor.close()
        db_pool.putconn(db_conn)


def get_teachers():
    """Get list of teachers for login dropdown"""
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    cursor.execute('SELECT teacher_id, first_name, last_name FROM teacher')
    rows = [{'id': c[0], 'name': '{} {}'.format(c[1], c[2])} for c in cursor]
    session['teachers'] = rows
    cursor.close()
    db_pool.putconn(db_conn)


def handle_error():
    """Take any live error from the session and set it on g"""
    g.error = session.pop('error', None)


@app.before_request
def before_request():
    handle_login()
    handle_error()
    get_teachers()


####################################
# TEACHER STUFF
##################################
@app.route('/addteacher', methods=['GET', 'POST'])
def addTeacher():
    """display add teacher form"""
    addTeacherForm = TeacherForm()
    return render_template('addteacher.html', addTeacherForm=addTeacherForm)


@app.route('/saveAddTeacher', methods=['POST'])
def saveAddTeacher():
    """process add teacher form"""
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    telephone = request.form['telephone']
    email = request.form['email']

    newteacher = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "telephone": telephone}

    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()
    sql = f'''INSERT INTO teacher
    (first_name, last_name, email, telephone)
    VALUES (%s, %s, %s, %s) RETURNING teacher_id AS last_id;'''
    cursor.execute(sql,
                   (newteacher['first_name'],
                    newteacher["last_name"],
                    newteacher["email"],
                    newteacher["telephone"]))
    db_conn.commit()
    teacher_id = cursor.fetchall()[0][0]
    cursor.close()
    db_pool.putconn(db_conn)

    return redirect(url_for('renderTeachers', teacher_id=teacher_id))


@app.route('/', methods=['GET', 'POST'])
@app.route('/<teacher_id>', methods=['GET', 'POST'])
def renderTeachers(teacher_id=None):
    """display teacher courses"""
    if not teacher_id:
        teacher_id = str(session.get('user')['id'])
    else:
        login(teacher_id)

    db_conn = db_pool.getconn()
    dict_cur = db_conn.cursor(cursor_factory=extras.RealDictCursor)
    dict_cur.execute('''
        SELECT c.course_id, title, COUNT(student_id)
        AS student_count FROM course c
        LEFT JOIN student_course sc on c.course_id = sc.course_id
        WHERE c.teacher = %s
        GROUP BY c.course_id
        ORDER BY title
        ''', teacher_id)

    courses = dict_cur.fetchall()

    dict_cur.close()
    db_pool.putconn(db_conn)

    return render_template('index.html', courses=courses)


@app.route('/editTeacher/<teacher_id>', methods=['GET', 'POST'])
def editTeacher(teacher_id):
    """display edit teacher form"""
    db_conn = db_pool.getconn()
    dict_cur = db_conn.cursor(cursor_factory=extras.DictCursor)
    dict_cur.execute(f'SELECT * FROM teacher '
                     f'WHERE teacher_id = {teacher_id}')
    teacher = dict_cur.fetchone()
    dict_cur.close()
    db_pool.putconn(db_conn)

    editTeacherForm = TeacherForm()
    return render_template(
        'editteacher.html',
        editTeacherForm=editTeacherForm,
        teacher=teacher)


@app.route('/saveEditTeacher/<teacher_id>', methods=['POST'])
def saveEditTeacher(teacher_id):
    """process edit teacher form"""
    form = TeacherForm(request.form)
    teacher = {}
    if request.method == 'POST' and form.validate():
        teacher["first_name"] = request.form['first_name']
        teacher["last_name"] = request.form['last_name']
        teacher["email"] = request.form['email']
        teacher["telephone"] = request.form['telephone']
        db_conn = db_pool.getconn()
        cursor = db_conn.cursor()
        cursor.execute(
            f"UPDATE teacher SET first_name = %s, "
            f"last_name = %s, email = %s, telephone = %s "
            f"WHERE teacher_id = %s;",
            (teacher['first_name'],
             teacher['last_name'],
             teacher['email'],
             teacher['telephone'],
             teacher_id))

        db_conn.commit()
        cursor.close()
        db_pool.putconn(db_conn)

    return redirect(url_for('renderTeachers', teacher_id=teacher_id))


@app.route('/deleteTeacher/<teacher_id>', methods=['POST'])
def deleteTeacher(teacher_id):
    """process delete teacher"""
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()
    sql = f'''DELETE FROM teacher WHERE teacher_id = {teacher_id};'''
    cursor.execute(sql)
    db_conn.commit()

    # update session to be logged in as next teacher
    # a logout page would make more sense
    cursor.execute('SELECT teacher_id, first_name, last_name FROM teacher')
    row = cursor.fetchone()
    session['user'] = {
        'id': str(
            row[0]), 'name': '{} {}'.format(
            row[1], row[2])}
    cursor.execute('SELECT teacher_id, first_name, last_name FROM teacher')
    rows = [{'id': c[0], 'name': '{} {}'.format(c[1], c[2])} for c in cursor]
    session['teachers'] = rows

    cursor.close()
    db_pool.putconn(db_conn)

    return redirect(url_for('renderTeachers'))


###########################################
# STUDENT STUFF
# Add New Student Form
###########################################
@app.route('/addstudent/<course_id>', methods=['GET', 'POST'])
def addStudent(course_id):
    "displays add student form"
    addStudentForm = StudentForm()
    return render_template(
        'addstudent.html',
        addStudentForm=addStudentForm,
        course_id=course_id)


@app.route('/saveAddStudent/<course_id>', methods=['POST'])
def saveAddStudent(course_id):
    "process add student form"
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    telephone = request.form['telephone']
    year = request.form['year']

    newstudent = {"first_name": first_name, "last_name": last_name,
                  "email": email, "telephone": telephone, "year": year}

    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    cursor.execute(
        f"INSERT INTO student (first_name, last_name, "
        f"email, telephone, year) "
        f"VALUES (%s, %s, %s, %s, %s) RETURNING student_id AS last_id;",
        (newstudent['first_name'],
         newstudent["last_name"],
         newstudent["email"],
         newstudent["telephone"],
         newstudent["year"]))

    db_conn.commit()

    student_id = cursor.fetchall()[0][0]
    sql = f'''INSERT INTO student_course (student_id, course_id)
            VALUES (%s, %s);'''
    cursor.execute(sql, (student_id, course_id))
    db_conn.commit()
    cursor.close()
    db_pool.putconn(db_conn)

    return redirect(url_for('view_course', course_id=course_id))


@app.route('/student/<student_id>/<course_id>', methods=['GET', 'POST'])
def student(student_id, course_id):
    "display student submissions and courses"
    db_conn = db_pool.getconn()
    dict_cur = db_conn.cursor(cursor_factory=extras.DictCursor)
    dict_cur.execute(f'''
        SELECT student.student_id, student_course.course_id,
        assignment.title, submission.submission_id, first_name,
        last_name, grade, submitted, assignment
        FROM submission
        INNER JOIN student_submission
        ON student_submission.submission_id = submission.submission_id
        INNER JOIN student
        ON student.student_id = student_submission.student_id
        INNER JOIN student_course
        ON student.student_id = student_course.student_id
        INNER JOIN assignment
        ON submission.assignment = assignment.assignment_id
        WHERE student.student_id = {student_id}
        AND student_course.course_id = {course_id};
        ''')
    submissions = dict_cur.fetchall()
    if not len(submissions):
        dict_cur.execute(f'''
            SELECT student.student_id, student_course.course_id,
            first_name, last_name
            FROM student
            INNER JOIN student_course
            ON student.student_id = student_course.student_id
            WHERE student.student_id = {student_id}
            AND student_course.course_id = {course_id};
            ''')
        submissions = dict_cur.fetchall()

    dict_cur = db_conn.cursor(cursor_factory=extras.DictCursor)
    dict_cur.execute(
        f"SELECT student.student_id, teacher.teacher_id, "
        f"teacher.first_name AS teacher_first_name, "
        f"teacher.last_name AS teacher_last_name, "
        f"course.course_id, course.title "
        f"FROM student "
        f"INNER JOIN student_course "
        f"ON student_course.student_id = student.student_id "
        f"INNER JOIN course on course.course_id = student_course.course_id "
        f"INNER JOIN teacher on course.teacher = teacher.teacher_id "
        f"WHERE student.student_id = {student_id}")
    courses = dict_cur.fetchall()
    if len(courses):
        print(courses)
    else:
        dict_cur = db_conn.cursor(cursor_factory=extras.DictCursor)
        dict_cur.execute(
            f"SELECT * FROM student WHERE student_id={student_id};")
        courses = dict_cur.fetchall()
        print(courses)

    dict_cur.close()
    db_pool.putconn(db_conn)

    return render_template(
        'student.html',
        submissions=submissions,
        courses=courses)


@app.route('/editstudent/<student_id>/<course_id>', methods=['GET', 'POST'])
def editStudent(student_id, course_id):
    """display edit student form"""
    db_conn = db_pool.getconn()
    dict_cur = db_conn.cursor(cursor_factory=extras.DictCursor)
    dict_cur.execute(f'SELECT * FROM student WHERE student_id = {student_id}')
    student = dict_cur.fetchone()
    dict_cur.close()
    db_pool.putconn(db_conn)

    editStudentForm = StudentForm()
    return render_template(
        'editstudent.html',
        editStudentForm=editStudentForm,
        student=student,
        course_id=course_id)


@app.route('/saveEditStudent/<course_id>/<student_id>', methods=['POST'])
def saveEditStudent(course_id, student_id):
    """process edit student form"""
    form = StudentForm(request.form)
    student = {}
    if request.method == 'POST' and form.validate():
        student["first_name"] = request.form['first_name']
        student["last_name"] = request.form['last_name']
        student["year"] = request.form['year']
        student["email"] = request.form['email']
        student["telephone"] = request.form['telephone']
        db_conn = db_pool.getconn()
        cursor = db_conn.cursor()
        cursor.execute(
            f"UPDATE student SET first_name = %s, "
            f"last_name = %s, year = %s, email = %s, "
            f"telephone = %s WHERE student_id = %s;",
            (student['first_name'],
             student['last_name'],
             student['year'],
             student['email'],
             student['telephone'],
             student_id))

        db_conn.commit()
        cursor.close()
        db_pool.putconn(db_conn)

    return redirect(
        url_for(
            'student',
            student_id=student_id,
            course_id=course_id))


@app.route('/deleteStudent/<student_id>/<course_id>', methods=['POST'])
def deleteStudent(student_id, course_id):
    """process delete student"""
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()
    sql = f'''DELETE FROM student_course
    WHERE student_id={student_id} and course_id={course_id};'''
    cursor.execute(sql)
    db_conn.commit()
    cursor.close()
    db_pool.putconn(db_conn)

    return redirect(url_for('view_course', course_id=course_id))

#################################
# Assignment Stuff
################################
@app.route('/addassignment/<course>', methods=['GET', 'POST'])
def addAssignment(course):
    """display add assignment form"""
    db_conn = db_pool.getconn()
    dict_cur = db_conn.cursor(cursor_factory=extras.DictCursor)

    addAssignmentForm = AssignmentForm()

    dict_cur.close()
    db_pool.putconn(db_conn)

    return render_template(
        'addassignment.html',
        addAssignmentForm=addAssignmentForm,
        course_id=course)


@app.route('/saveAddAssignment/<course_id>', methods=['POST'])
def saveAddAssignment(course_id):
    """process add student form"""
    title = request.form['title']
    due = request.form['due']
    points = request.form['points']
    description = request.form['description']

    newassignment = {
        "title": title,
        "due": due,
        "points": points,
        "description": description
    }

    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()
    sql = f'''INSERT INTO assignment
    (title, due, points, description, course)
    VALUES (%s, %s, %s, %s, %s);'''
    cursor.execute(sql,
                   (newassignment['title'],
                    newassignment["due"],
                    newassignment["points"],
                    newassignment["description"],
                    course_id))

    db_conn.commit()
    cursor.close()
    db_pool.putconn(db_conn)

    return redirect(url_for('view_course', course_id=course_id))


@app.route('/assignment/<assignment_id>/<course_id>', methods=['GET', 'POST'])
def assignment(assignment_id, course_id):
    """display assignment details and submissions"""
    db_conn = db_pool.getconn()
    dict_cur = db_conn.cursor(cursor_factory=extras.DictCursor)
    dict_cur.execute(f'''
        SELECT student.student_id, student_course.course_id,
        assignment.title, submission.submission_id, first_name,
        last_name, grade, submitted, assignment AS assignment_id,
        course.title AS course_title,
        assignment.description, assignment.points, assignment.due
        FROM submission
        INNER JOIN student_submission
        ON student_submission.submission_id = submission.submission_id
        INNER JOIN student
        ON student.student_id = student_submission.student_id
        INNER JOIN student_course
        ON student.student_id = student_course.student_id
        INNER JOIN course
        ON student_course.course_id = course.course_id
        INNER JOIN assignment
        ON submission.assignment = assignment.assignment_id
        WHERE assignment.assignment_id = {assignment_id}
        AND student_course.course_id = {course_id};
        ''')
    submissions = dict_cur.fetchall()
    if not len(submissions):
        dict_cur.execute(f'''
            SELECT *, course as course_id FROM assignment
            WHERE assignment_id = {assignment_id}
            ''')
        submissions = dict_cur.fetchall()

    dict_cur.close()
    db_pool.putconn(db_conn)

    return render_template('assignment.html', submissions=submissions)


@app.route(
    '/editassignment/<assignment_id>/<course_id>',
    methods=[
        'GET',
        'POST'])
def editAssignment(assignment_id, course_id):
    """display edit student form"""
    db_conn = db_pool.getconn()
    dict_cur = db_conn.cursor(cursor_factory=extras.DictCursor)
    dict_cur.execute(
        f'SELECT * FROM assignment WHERE assignment_id = {assignment_id}')
    assignment = dict_cur.fetchone()
    dict_cur.close()
    db_pool.putconn(db_conn)

    editAssignmentForm = AssignmentForm()
    return render_template(
        'editassignment.html',
        editAssignmentForm=editAssignmentForm,
        assignment=assignment,
        course_id=course_id)


@app.route('/saveEditAssignment/<course_id>/<assignment_id>', methods=['POST'])
def saveEditAssignment(course_id, assignment_id):
    """process edit student form"""
    form = AssignmentForm(request.form)
    assignment = {}
    if request.method == 'POST' and form.validate():
        assignment["title"] = request.form['title']
        assignment["description"] = request.form['description']
        assignment["points"] = request.form['due']
        assignment["due"] = request.form['points']
        db_conn = db_pool.getconn()
        cursor = db_conn.cursor()
        cursor.execute(
            f"UPDATE assignment SET title = %s, description = %s, "
            f"points = %s, due = %s "
            f"WHERE assignment_id = %s;",
            (assignment['title'],
             assignment['description'],
             assignment['due'],
             assignment['points'],
             assignment_id))

        db_conn.commit()
        cursor.close()
        db_pool.putconn(db_conn)

    return redirect(
        url_for(
            'assignment',
            assignment_id=assignment_id,
            course_id=course_id))


@app.route('/deleteAssignment/<assignment_id>/<course_id>', methods=['POST'])
def deleteAssignment(assignment_id, course_id):
    """process delete student"""
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()
    sql = f'''DELETE FROM assignment WHERE assignment_id={assignment_id};'''
    cursor.execute(sql)
    db_conn.commit()
    cursor.close()
    db_pool.putconn(db_conn)

    return redirect(url_for('view_course', course_id=course_id))

###############################
# COURSE STUFF
################################
@app.route('/addcourse/<teacher_id>', methods=['GET', 'POST'])
def addCourse(teacher_id):
    """display add course form"""
    addCourseForm = CourseForm()
    return render_template(
        'addcourse.html',
        addCourseForm=addCourseForm,
        teacher_id=teacher_id)


@app.route('/saveaddcourse/<teacher_id>', methods=['POST'])
def saveAddCourse(teacher_id):
    """process add course form"""
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
                    newcourse["section"],
                    newcourse["department"],
                    newcourse["description"],
                    newcourse["units"],
                    newcourse["teacher"]
                    ))
    db_conn.commit()
    cursor.close()
    db_pool.putconn(db_conn)

    return redirect(url_for('renderTeachers', teacher_id=teacher))


@app.route('/course/<course_id>', methods=['GET'])
def view_course(course_id):
    """display course details and roster"""
    db_conn = db_pool.getconn()
    dict_cur = db_conn.cursor(cursor_factory=extras.DictCursor)
    dict_cur.execute(f"SELECT * FROM course "
                     f"WHERE course_id = %s", course_id)
    course = dict_cur.fetchone()

    # perform search by first or last name or both
    name_q = request.args.get('name') or ''
    if name_q:
        # search for first OR last name
        name = '{}%'.format(name_q.lower())
        dict_cur.execute('''
            SELECT *
            FROM student
            INNER JOIN student_course
            ON student_course.student_id = student.student_id
            WHERE student_course.course_id = %s
            AND (LOWER(student.first_name) LIKE %s
            OR LOWER(student.last_name) LIKE %s)
            ''', (course_id, name, name))
        students = dict_cur.fetchall()
        # search for first AND last name
        if not len(students):
            first_name, last_name = name_q.split(
                ' ')[0].lower(), name_q.split(' ')[1].lower()
            dict_cur.execute('''
                SELECT *
                FROM student
                INNER JOIN student_course
                ON student_course.student_id = student.student_id
                WHERE student_course.course_id = %s
                AND (LOWER(student.first_name) LIKE %s
                AND LOWER(student.last_name) LIKE %s)
                ''', (course_id, first_name, last_name))
            students = dict_cur.fetchall()

    else:
        dict_cur.execute('''
            SELECT *
            FROM student
            INNER JOIN student_course
            ON student_course.student_id = student.student_id
            WHERE student_course.course_id = %s
            ''', course_id)
        students = dict_cur.fetchall()

    dict_cur.execute(f"SELECT * FROM assignment "
                     f"WHERE course = {course_id};")
    assignments = dict_cur.fetchall()

    grades = np.zeros((max(len(students), 1), max(len(assignments), 1)))
    submissions = np.zeros((max(len(students), 1), max(len(assignments), 1)))
    for i, assignment in enumerate(assignments):
        for j, student in enumerate(students):
            dict_cur.execute(
                f"SELECT student.student_id, assignment.assignment_id, "
                f"submission.submission_id, submission.grade "
                f"FROM student "
                f"LEFT OUTER JOIN student_submission "
                f"ON student.student_id = student_submission.student_id "
                f"LEFT OUTER JOIN submission "
                f"ON student_submission.submission_id "
                f"= submission.submission_id "
                f"LEFT OUTER JOIN assignment "
                f"ON submission.assignment "
                f"= assignment.assignment_id "
                f"WHERE student.student_id = {student['student_id']} "
                f"AND assignment.assignment_id "
                f"= {assignment['assignment_id']};")
            results = dict_cur.fetchall()
            print(results)
            if len(results):
                grades[j, i] = results[0][3]
                submissions[j, i] = results[0][2]
            else:
                grades[j, i] = None
                submissions[j, i] = 0
        print(grades)
    dict_cur.close()
    db_pool.putconn(db_conn)

    return render_template(
        'course.html',
        course=course,
        students=students,
        assignments=assignments,
        grades=grades,
        submissions=submissions,
        name=name_q,
        redirect_option="course")


@app.route('/editcourse/<course_id>', methods=['GET', 'POST'])
def editCourse(course_id):
    """display edit course form"""
    db_conn = db_pool.getconn()
    dict_cur = db_conn.cursor(cursor_factory=extras.DictCursor)
    dict_cur.execute(f'SELECT * FROM course '
                     f'WHERE course_id = {course_id}')
    course = dict_cur.fetchone()
    dict_cur.close()
    db_pool.putconn(db_conn)
    editCourseForm = CourseForm()

    return render_template(
        'editcourse.html',
        editCourseForm=editCourseForm,
        course=course)


@app.route('/saveEditCourse/<course_id>/<teacher_id>', methods=['POST'])
def saveEditCourse(course_id, teacher_id):
    """process course edit form"""
    form = CourseForm(request.form)
    course = {}
    if request.method == 'POST' and form.validate():
        course['title'] = request.form['title']
        course['section'] = request.form['section']
        course['department'] = request.form['department']
        course['description'] = request.form['description']
        course['units'] = request.form['units']

        db_conn = db_pool.getconn()
        cursor = db_conn.cursor()
        cursor.execute(
            f"UPDATE course SET title = %s, section = %s, department = %s, "
            f"description = %s, units = %s WHERE course_id = %s;",
            (course['title'],
             course['section'],
                course["department"],
                course["description"],
                course["units"],
                course_id))
        db_conn.commit()
        cursor.close()
        db_pool.putconn(db_conn)

    return redirect(url_for('renderTeachers', teacher_id=teacher_id))


@app.route('/deleteCourse/<course_id>/<teacher_id>', methods=['POST'])
def deleteCourse(course_id, teacher_id):
    """process delete course"""
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()
    sql = f'''DELETE FROM course WHERE course_id = {course_id};'''
    cursor.execute(sql)
    db_conn.commit()
    cursor.close()
    db_pool.putconn(db_conn)

    return redirect(url_for('renderTeachers', teacher_id=teacher_id))


##########################################
# SUBMISSION STUFF
########################################
@app.route('/submissions', methods=['GET'])
def viewsubmissions():
    """display submissions"""
    db_conn = db_pool.getconn()
    dict_cur = db_conn.cursor(cursor_factory=extras.DictCursor)
    dict_cur.execute('''
        SELECT student.student_id, submission.submission_id,
        first_name, last_name, grade, submitted, assignment
        FROM submission
        INNER JOIN student_submission
        ON student_submission.submission_id = submission.submission_id
        INNER JOIN student
        ON student.student_id = student_submission.student_id
        ORDER BY last_name ASC;
        ''')
    submissions = dict_cur.fetchall()

    dict_cur.close()
    db_pool.putconn(db_conn)
    return render_template('viewsubmissions.html', submissions=submissions)


@app.route(
    '/addsubmission/<course_id>/<assignment_id>/<student_id>',
    methods=[
        'GET',
        'POST'])
def addSubmission(course_id, assignment_id, student_id):
    """display add assignment form"""
    db_conn = db_pool.getconn()
    dict_cur = db_conn.cursor(cursor_factory=extras.DictCursor)

    addSubmissionForm = SubmissionForm()

    dict_cur.close()
    db_pool.putconn(db_conn)

    return render_template(
        'addsubmission.html',
        submission_form=addSubmissionForm,
        course_id=course_id,
        assignment_id=assignment_id,
        student_id=student_id)


@app.route(
    '/saveAddSubmission/<course_id>/<assignment_id>/<student_id>',
    methods=['POST'])
def saveAddSubmission(course_id, assignment_id, student_id):
    """process add student form"""
    grade = request.form['grade']
    sub_date = request.form['sub_time']

    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()
    sql = f'''INSERT INTO submission
    (grade, submitted, assignment)
    VALUES (%s, %s, %s)
    RETURNING submission_id AS last_id;'''
    cursor.execute(sql,
                   (grade,
                    sub_date,
                    assignment_id))
    db_conn.commit()
    submission_id = cursor.fetchall()[0][0]

    sql = f'''INSERT INTO student_submission
    (student_id, submission_id)
    VALUES (%s, %s);'''
    cursor.execute(sql,
                   (student_id,
                    submission_id))
    db_conn.commit()
    cursor.close()
    db_pool.putconn(db_conn)

    return redirect(url_for('view_course', course_id=course_id))


@app.route(
    '/editsubmission/<submission_id>/<course_id>/'
    '<item_id>/<redirect_option>',
    methods=['GET', 'POST'])
def editSubmission(submission_id, course_id, item_id, redirect_option):
    """display edit submission form"""
    db_conn = db_pool.getconn()
    dict_cur = db_conn.cursor(cursor_factory=extras.DictCursor)
    dict_cur.execute(
        f'''SELECT * FROM submission
WHERE submission_id = {submission_id}''')
    submission = dict_cur.fetchone()
    dict_cur.close()
    db_pool.putconn(db_conn)

    editSubmissionForm = SubmissionForm()
    return render_template(
        'editsubmission.html',
        editSubmissionForm=editSubmissionForm,
        submission=submission,
        course_id=course_id,
        item_id=item_id,
        redirect_option=redirect_option)


@app.route(
    '/saveEditSubmission/<submission_id>/<course_id>/'
    '<item_id>/<redirect_option>',
    methods=['POST'])
def saveEditSubmission(submission_id, course_id, item_id, redirect_option):
    """process submission form"""
    form = SubmissionForm(request.form)
    submission = {}
    if request.method == 'POST' and form.validate():
        print(form)
        submission['submitted'] = request.form['sub_time']
        submission['grade'] = request.form['grade']
        db_conn = db_pool.getconn()
        cursor = db_conn.cursor()
        cursor.execute(
            f"UPDATE submission SET grade = %s, submitted = %s "
            f"WHERE submission_id = %s; ",
            (submission['grade'],
             submission['submitted'],
             submission_id))
        db_conn.commit()
        cursor.close()
        db_pool.putconn(db_conn)

    if redirect_option == "student":
        return redirect(
            url_for(
                'student',
                student_id=item_id,
                course_id=course_id))
    elif redirect_option == "assignment":
        return redirect(
            url_for(
                'assignment',
                assignment_id=item_id,
                course_id=course_id))
    else:
        return redirect(
            url_for(
                'view_course',
                course_id=course_id))


@app.route(
    '/deleteSubmission/<submission_id>/<item_id>/'
    '<course_id>/<redirect_option>',
    methods=['POST'])
def deleteSubmission(submission_id, item_id, course_id, redirect_option):
    """process submission delete"""
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()
    sql = f'''DELETE FROM submission
WHERE submission_id = {submission_id};'''
    cursor.execute(sql)
    db_conn.commit()
    cursor.close()
    db_pool.putconn(db_conn)

    if redirect_option == "student":
        return redirect(
            url_for(
                'student',
                student_id=item_id,
                course_id=course_id))
    else:
        return redirect(
            url_for(
                'assignment',
                assignment_id=item_id,
                course_id=course_id))


# Login route
@app.route('/login/<id>', methods=['GET'])
def login(id):
    db_conn = db_pool.getconn()
    cursor = db_conn.cursor()

    cursor.execute(
        'SELECT teacher_id, first_name, last_name '
        'FROM teacher WHERE teacher_id = %s',
        id)
    row = cursor.fetchone()
    if not row:
        abort(404, 'No teacher found for id')

    session['user'] = {'id': row[0],
                       'name': '{} {}'.format(row[1], row[2])}

    cursor.close()
    db_pool.putconn(db_conn)

    return redirect(url_for('renderTeachers'))


# Admin page
@app.route('/admin', methods=['GET'])
@app.route('/admin/<table>', methods=['GET', 'POST'])
def viewadmin(table=None):

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

        if table not in table_names:
            abort(404, 'Invalid table name')

        dict_cur = db_conn.cursor(cursor_factory=extras.DictCursor)
        dict_cur.execute(
            sql.SQL('SELECT * FROM {}').format(sql.Identifier(table))
        )
        columns = [desc[0] for desc in dict_cur.description]
        records = dict_cur.fetchall()
        dict_cur.close()

        db_pool.putconn(db_conn)

        return render_template(
            'admin.html',
            table=records,
            columns=columns,
            table_names=table_names,
            title=table)
    else:
        values = [v if v != '' else None for v in request.form.values()]

        cur = db_conn.cursor()
        try:
            cur.execute(
                sql.SQL('INSERT INTO {} VALUES ({})').format(
                    sql.Identifier(table),
                    sql.SQL(', ').join(sql.Placeholder() * len(values))
                ),
                values
            )
            db_conn.commit()
        except Exception as err:
            session['error'] = str(err)
            db_conn.rollback()

        cur.close()
        db_pool.putconn(db_conn)

        return redirect('/admin/{}'.format(table))
