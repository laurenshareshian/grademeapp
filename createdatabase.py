from psycopg2 import connect, extensions
from urllib.parse import urlparse
import time
from seed_database import seed


def createdatabase(database_url):
    result = urlparse(database_url)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port
    print(
        'connecting to database',
        username,
        password,
        database,
        hostname,
        port)
    conn = connect(
        database=database,
        user=username,
        password=password,
        host=hostname,
        port=port
    )

    # get the isolation level for autocommit
    # set the isolation level for the connection's cursors
    # will raise ActiveSqlTransaction exception otherwise
    autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
    conn.set_isolation_level(autocommit)

    # instantiate a cursor object from the connection
    cursor = conn.cursor()

    # Create student table

    sql = "DROP TABLE IF EXISTS student;"
    cursor.execute(sql)
    conn.commit()

    cursor = conn.cursor()
    sql = '''CREATE TABLE student(
       student_id        SERIAL       PRIMARY KEY,
       first_name        CHAR(50)     NOT NULL,
       last_name         CHAR(50)     NOT NULL,
       year              INT          NOT NULL,
       email             CHAR(50)     NOT NULL,
       telephone         CHAR(10)
    );
    '''
    cursor.execute(sql)
    conn.commit()


    # Create teacher table

    sql = f"DROP TABLE IF EXISTS teacher;"
    cursor.execute(sql)
    conn.commit()

    cursor = conn.cursor()
    sql = '''CREATE TABLE teacher(
       teacher_id        SERIAL       PRIMARY KEY,
       first_name        CHAR(50)     NOT NULL,
       last_name         CHAR(50)     NOT NULL,
       email             CHAR(50)     NOT NULL,
       telephone         CHAR(10)
    );
    '''
    cursor.execute(sql)
    conn.commit()


    # Create course table

    sql = f"DROP TABLE IF EXISTS course;"
    cursor.execute(sql)
    conn.commit()

    cursor = conn.cursor()
    sql = '''CREATE TABLE course(
       course_id        SERIAL       PRIMARY KEY,
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


    # Create assignment table

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


    # Create submission table

    cursor.execute('DROP TABLE IF EXISTS submission;')
    cursor.execute('''CREATE TABLE submission(
        submission_id   SERIAL PRIMARY KEY,
        submitted       TIMESTAMP,
        grade           INT,
        assignment      INT
        CONSTRAINT valid_grade CHECK(0 <= grade AND grade <= 100)
    );''')


    # Create student_submission table

    cursor.execute('DROP TABLE IF EXISTS student_submission;')
    cursor.execute('''CREATE TABLE student_submission(
      student_id      INT,
      submission_id   INT,
      PRIMARY KEY (student_id, submission_id)
      );''')
    conn.commit()


    # Create student_course table

    cursor.execute('DROP TABLE IF EXISTS student_course;')
    cursor.execute('''CREATE TABLE student_course(
      course_id   INT,
      student_id  INT,
      PRIMARY KEY (course_id, student_id)
      );''')
    conn.commit()


    # seed database
    seed(cursor)
    conn.commit()

    # close the cursor to avoid memory leaks
    cursor.close()

    # close the connection to avoid memory leaks
    conn.close()
