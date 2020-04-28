# import the psycopg2 database adapter for PostgreSQL
from psycopg2 import connect, extensions, sql
from urllib.parse import urlparse
from config import Config


def createdatabase(database_url):
    result = urlparse(database_url)
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

    # get the isolation level for autocommit
    # set the isolation level for the connection's cursors
    # will raise ActiveSqlTransaction exception otherwise
    autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
    conn.set_isolation_level( autocommit )

    # instantiate a cursor object from the connection
    cursor = conn.cursor()

    # sql = f"DROP TABLE IF EXISTS students;"
    # cursor.execute(sql)
    # conn.commit()


    # cursor = conn.cursor()
    # sql = '''CREATE TABLE students(
    #    STUDENTID SERIAL PRIMARY KEY,
    #    FIRST        CHAR(50)     NOT NULL,
    #    LAST         CHAR(50)     NOT NULL,
    #    EMAIL        CHAR(50)
    # );
    # '''
    # cursor.execute(sql)
    # conn.commit()
    #
    # cursor.execute(
    #    "INSERT INTO students (FIRST,LAST,EMAIL) "
    #    "VALUES ('Lauren','Shareshian','lauren@gmail.com');"
    # )
    # conn.commit()
    # cursor.execute(
    #    "INSERT INTO students (FIRST,LAST,EMAIL) "
    #    "VALUES ('Paul','OGDEN','lauren@gmail.com');"
    # )
    # conn.commit()
    #
    # cursor.execute("SELECT * FROM students;")
    # rows = cursor.fetchall()
    # print(rows)

    sql = f"DROP TABLE IF EXISTS teacher;"
    cursor.execute(sql)
    conn.commit()

    cursor = conn.cursor()
    sql = '''CREATE TABLE teacher(
       teacher_id        SERIAL PRIMARY KEY,
       first_name        CHAR(50)     NOT NULL,
       last_name         CHAR(50)     NOT NULL,
       email             CHAR(50)     NOT NULL,
       telephone         CHAR(10)     NOT NULL
    );
    '''
    cursor.execute(sql)
    conn.commit()

    cursor.execute(
       "INSERT INTO teacher (first_name, last_name, email, telephone) "
       "VALUES ('Lauren','Shareshian','lauren@gmail.com', '6094397996');"
    )
    cursor.execute(
       "INSERT INTO teacher (first_name, last_name, email, telephone) "
       "VALUES ('Joshua','Cox','cox@gmail.com', '5555555555');"
    )

    sql = f"DROP TABLE IF EXISTS student;"
    cursor.execute(sql)
    conn.commit()

    cursor = conn.cursor()
    sql = '''CREATE TABLE student(
       student_id        SERIAL PRIMARY KEY,
       first_name        CHAR(50)     NOT NULL,
       last_name         CHAR(50)     NOT NULL,
       year              INT          NOT NULL,
       email             CHAR(50)     NOT NULL,
       telephone         CHAR(10)     NOT NULL 
    );
    '''
    cursor.execute(sql)
    conn.commit()

    cursor.execute(
       "INSERT INTO student (first_name, last_name, year, email, telephone) "
       "VALUES ('Kanye', 'West',2020, 'kanye@gmail.com', '6094397996');"
    )
    cursor.execute(
       "INSERT INTO student (first_name, last_name, year, email, telephone) "
       "VALUES ('Anthony', 'Fauci', 2021, 'fauci@gmail.com', '5555555555');"
    )

    sql = f"DROP TABLE IF EXISTS course;"
    cursor.execute(sql)
    conn.commit()

    cursor = conn.cursor()
    sql = '''CREATE TABLE course(
       course_id        SERIAL PRIMARY KEY,
       title            CHAR(50)     NOT NULL,
       section          INT     NOT NULL,
       department       CHAR(50)          NOT NULL,
       description      CHAR(200)     NOT NULL,
       units            INT     NOT NULL    
    );
    '''
    cursor.execute(sql)
    conn.commit()

    cursor.execute(
       "INSERT INTO course (title, section, department, description, units) "
       "VALUES ('Calculus', '100', 'Math', 'Integrals', 4);"
    )
    cursor.execute(
       "INSERT INTO course (title, section, department, description, units) "
       "VALUES ('Basketweaving', '400', 'Art', 'Weaving stuff', 3);"
    )

    sql = f"DROP TABLE IF EXISTS assignment;"
    cursor.execute(sql)
    conn.commit()

    cursor = conn.cursor()
    sql = '''CREATE TABLE assignment(
       assignment_id        SERIAL PRIMARY KEY,
       title            CHAR(50)     NOT NULL,
       description      CHAR(200)     NOT NULL,
       due              DATE            NOT NULL,
       points            INT     NOT NULL    
    );
    '''
    cursor.execute(sql)
    conn.commit()

    cursor.execute(
       "INSERT INTO assignment (title, description, due, points) "
       "VALUES ('HW 1', 'Book exercises', '2020-01-01', 5);"
    )
    cursor.execute(
       "INSERT INTO assignment (title, description, due, points) "
       "VALUES ('Essay', 'Faulkner essay', '2020-01-02', 50);"
    )

    # close the cursor to avoid memory leaks
    cursor.close()

    # close the connection to avoid memory leaks
    conn.close()