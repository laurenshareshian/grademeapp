# import the psycopg2 database adapter for PostgreSQL
from psycopg2 import connect, extensions, sql
from urllib.parse import urlparse

def createdatabase():
    #result = urlparse("postgresql://objectrocket:mypass@localhost/postgres") local database
    result = urlparse("postgres://dnksgzdceixveu:e9289a3cd88b80874ba424a0e5f14c20113572f675cedc70a4cb5b94ba875c3a@ec2-18-206-84-251.compute-1.amazonaws.com:5432/dq7nmi44nhj5q")
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

    sql = f"DROP TABLE IF EXISTS students;"
    cursor.execute(sql)
    conn.commit()


    cursor = conn.cursor()
    sql = '''CREATE TABLE students(
       STUDENTID SERIAL PRIMARY KEY,
       FIRST        CHAR(50)     NOT NULL,
       LAST         CHAR(50)     NOT NULL,
       EMAIL        CHAR(50)
    );
    '''
    cursor.execute(sql)
    conn.commit()

    cursor.execute(
       "INSERT INTO students (FIRST,LAST,EMAIL) "
       "VALUES ('Lauren','Shareshian','lauren@gmail.com');"
    )
    conn.commit()
    cursor.execute(
       "INSERT INTO students (FIRST,LAST,EMAIL) "
       "VALUES ('Paul','OGDEN','lauren@gmail.com');"
    )
    conn.commit()

    cursor.execute("SELECT * FROM students;")
    rows = cursor.fetchall()
    print(rows)

    # close the cursor to avoid memory leaks
    cursor.close()

    # close the connection to avoid memory leaks
    conn.close()