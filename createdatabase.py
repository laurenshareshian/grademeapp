# import the psycopg2 database adapter for PostgreSQL
from psycopg2 import connect, extensions, sql
from urllib.parse import urlparse
from config import Config
import time

def createdatabase(database_url):
    result = urlparse(database_url)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port
    print('connecting to database', username, password, database, hostname, port)
    conn = connect(
        database = database,
        user = username,
        password = password,
        host = hostname,
        port = port
    )

    # get the isolation level for autocommit
    # set the isolation level for the connection's cursors
    # will raise ActiveSqlTransaction exception otherwise
    autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
    conn.set_isolation_level( autocommit )

    # instantiate a cursor object from the connection
    cursor = conn.cursor()

    ## Create student table


    sql = f"DROP TABLE IF EXISTS student;"
    cursor.execute(sql)
    print('here')
    conn.commit()


    cursor = conn.cursor()
    sql = '''CREATE TABLE student(
       student_id SERIAL PRIMARY KEY,
       first_name        CHAR(50)     NOT NULL,
       last_name         CHAR(50)     NOT NULL,
       year              INT          NOT NULL,
       email             CHAR(50)     NOT NULL,
       telephone         CHAR(10)
    );
    '''
    cursor.execute(sql)
    conn.commit()

    cursor.execute(
       "INSERT INTO student (first_name, last_name, year, email, telephone) "
       "VALUES ('Kanye', 'West',2020, 'kanye@gmail.com', '6094397996');"
    )
    conn.commit()

    cursor.execute(
       "INSERT INTO student (first_name, last_name, year, email, telephone) "
       "VALUES ('Anthony', 'Fauci', 2021, 'fauci@gmail.com', '5555555555');"
    )
    conn.commit()

    cursor.execute(
       "INSERT INTO student (first_name, last_name, year, email, telephone) "
       "VALUES ('Tiger', 'King', 2021, 'iluvtigers@gmail.com', '5555555555');"
    )
    conn.commit()

    cursor.execute(
       "INSERT INTO student (first_name, last_name, year, email, telephone) "
       "VALUES ('Lion', 'King', 2021, 'iluvlionss@gmail.com', '5555555555');"
    )
    conn.commit()

    ## Create teacher table


    sql = f"DROP TABLE IF EXISTS teacher;"
    cursor.execute(sql)
    conn.commit()

    cursor = conn.cursor()
    sql = '''CREATE TABLE teacher(
       teacher_id SERIAL PRIMARY KEY,
       first_name        CHAR(50)     NOT NULL,
       last_name         CHAR(50)     NOT NULL,
       email             CHAR(50)     NOT NULL,
       telephone         CHAR(10)
    );
    '''
    cursor.execute(sql)
    conn.commit()

    cursor.execute(
       "INSERT INTO teacher (first_name, last_name, email, telephone) "
       "VALUES ('Lauren','Shareshian','lauren@gmail.com', '6094397996');"
    )
    conn.commit()

    cursor.execute(
       "INSERT INTO teacher (first_name, last_name, email, telephone) "
       "VALUES ('Joshua','Cox','cox@gmail.com', '5555555555');"
    )
    conn.commit()

    cursor.execute(
       "INSERT INTO teacher (first_name, last_name, email, telephone) "
       "VALUES ('Elon','Musk Baby','baby@gmail.com', '5555555555');"
    )
    conn.commit()

    cursor.execute(
       "INSERT INTO teacher (first_name, last_name, email, telephone) "
       "VALUES ('5G','Conspiracy Theorist','5G@gmail.com', '5555555555');"
    )
    conn.commit()

    ## Create course table


    sql = f"DROP TABLE IF EXISTS course;"
    cursor.execute(sql)
    conn.commit()

    cursor = conn.cursor()
    sql = '''CREATE TABLE course(
       course_id        SERIAL PRIMARY KEY,
       title            CHAR(50)     NOT NULL,
       section          INT          NOT NULL,
       department       CHAR(50)     NOT NULL,
       description      CHAR(200)    NOT NULL,
       units            INT          NOT NULL,
       teacher          INT
    );
    '''
    cursor.execute(sql)
    conn.commit()

    cursor.execute(
       "INSERT INTO course (title, section, department, description, units, teacher) "
       "VALUES ('Calculus', '100', 'Math', 'Integrals', 4, 1);"
    )
    conn.commit()
    cursor.execute(
       "INSERT INTO course (title, section, department, description, units, teacher) "
       "VALUES ('Basketweaving', '400', 'Art', 'Weaving stuff', 3, 2);"
    )
    conn.commit()
    cursor.execute(
       "INSERT INTO course (title, section, department, description, units, teacher) "
       "VALUES ('Algebra', '100', 'Math', 'Functions', 3, 1);"
    )
    conn.commit()

    cursor.execute(
       "INSERT INTO course (title, section, department, description, units) "
       "VALUES ('Advanced Tickling', '100', 'HR Problems', 'Creepy stuff', 5);"
    )
    conn.commit()

    cursor.execute(
       "INSERT INTO course (title, section, department, description, units, teacher) "
       "VALUES ('Expensive Remote Learning Course', '100', 'Science', 'same price as an in-person class without any labs', 5, 3);"
    )
    conn.commit()

    cursor.execute(
       "INSERT INTO course (title, section, department, description, units, teacher) "
       "VALUES ('Electricity', '100', 'Science', 'electricity stuff', 5, 4);"
    )
    conn.commit()

    ## Create assignment table


    sql = f"DROP TABLE IF EXISTS assignment;"
    cursor.execute(sql)
    conn.commit()

    cursor = conn.cursor()
    sql = '''CREATE TABLE assignment(
       assignment_id    SERIAL      PRIMARY KEY,
       title            CHAR(50)    NOT NULL,
       description      CHAR(200)   NOT NULL,
       due              DATE        NOT NULL,
       points           INT         NOT NULL,
       course           INT
    );
    '''
    cursor.execute(sql)
    conn.commit()

    cursor.execute(
       "INSERT INTO assignment (title, description, due, points, course) "
       "VALUES ('HW 1', 'Book exercises', '2020-01-01', 5, 1);"
    )
    conn.commit()
    cursor.execute(
       "INSERT INTO assignment (title, description, due, points, course) "
       "VALUES ('Test 1', 'Derivatives', '2020-01-02', 50, 1);"
    )
    conn.commit()
    cursor.execute(
       "INSERT INTO assignment (title, description, due, points, course) "
       "VALUES ('Exam 1', 'Slope', '2020-01-02', 50, 3);"
    )
    conn.commit()

    cursor.execute(
       "INSERT INTO assignment (title, description, due, points, course) "
       "VALUES ('Basket 1', 'basket', '2020-01-02', 100, 2);"
    )
    conn.commit()

    cursor.execute(
       "INSERT INTO assignment (title, description, due, points, course) "
       "VALUES ('Foot tickle', 'ticle', '2020-01-02', 100, 4);"
    )
    conn.commit()

    cursor.execute(
       "INSERT INTO assignment (title, description, due, points, course) "
       "VALUES ('HW Exercises', 'chapter 1', '2020-01-02', 100, 6);"
    )
    conn.commit()

    ### Create submission table


    cursor.execute('DROP TABLE IF EXISTS submission;')
    cursor.execute('''CREATE TABLE submission(
        submission_id   SERIAL PRIMARY KEY,
        submitted       TIMESTAMP,
        grade           INT,
        assignment      INT
        CONSTRAINT valid_grade CHECK(0 <= grade AND grade <= 100)
    );''')

    datetime_now = time.strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('''
        INSERT INTO submission (submitted, grade, assignment)
        VALUES (%s, %s, %s);
        ''',
        (datetime_now, 55, 1))

    cursor.execute('''
        INSERT INTO submission (submitted, grade, assignment)
        VALUES (%s, %s, %s);
        ''',
        (datetime_now, 72, 1))

    cursor.execute('''
        INSERT INTO submission (submitted, grade, assignment)
        VALUES (%s, %s, %s);
        ''',
        (datetime_now, 90, 2))




    cursor.execute('''
        INSERT into submission (submitted, grade)
        VALUES (NULL, NULL);
        ''')
    conn.commit()

    cursor.execute('''
        INSERT INTO submission (submitted, grade, assignment)
        VALUES (%s, %s, %s);
        ''',
        (datetime_now, 60, 3))

    ### Create student_submission table

    cursor.execute('DROP TABLE IF EXISTS student_submission;')
    cursor.execute('''CREATE TABLE student_submission(
      student_id      INT,
      submission_id   INT,
      PRIMARY KEY (student_id, submission_id)
      );''')
    conn.commit()

    cursor.execute('''
        INSERT into student_submission (student_id, submission_id)
        VALUES (1, 2), (1, 3), (2, 1), (2, 4), (1, 5);
        ''')
    conn.commit()

    ### Create student_course table


    cursor.execute('DROP TABLE IF EXISTS student_course;')
    cursor.execute('''CREATE TABLE student_course(
      course_id   INT,
      student_id  INT,
      PRIMARY KEY (course_id, student_id)
      );''')
    conn.commit()


    cursor.execute('''
        INSERT into student_course (student_id, course_id)
        VALUES (1, 1), (1, 2), (1, 3), (2, 1), (3, 1), (2, 3), (3, 5);
        ''')
    conn.commit()

    # close the cursor to avoid memory leaks
    cursor.close()

    # close the connection to avoid memory leaks
    conn.close()