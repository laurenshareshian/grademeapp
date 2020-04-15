# import the psycopg2 database adapter for PostgreSQL
from psycopg2 import connect, extensions, sql

# declare a new PostgreSQL connection object
conn = connect(
dbname = "postgres",
user = "objectrocket",
host = "localhost",
password = "mypass"
)

# get the isolation level for autocommit
# set the isolation level for the connection's cursors
# will raise ActiveSqlTransaction exception otherwise
autocommit = extensions.ISOLATION_LEVEL_AUTOCOMMIT
conn.set_isolation_level( autocommit )

# instantiate a cursor object from the connection
cursor = conn.cursor()

# use the execute() method to make a SQL request
cursor.execute(f"DROP DATABASE IF EXISTS grades;")
conn.commit()

# use the sql module instead to avoid SQL injection attacks
cursor.execute(sql.SQL(
"CREATE DATABASE {}"
).format(sql.Identifier( 'grades' )))

# close the cursor to avoid memory leaks
cursor.close()

# close the connection to avoid memory leaks
conn.close()

# connect to the new database
conn = connect(
dbname = "grades",
user = "objectrocket",
host = "localhost",
password = "mypsword"
)
cursor = conn.cursor()
sql = '''CREATE TABLE students(
   STUDENTID INT PRIMARY KEY     NOT NULL,
   FIRST        CHAR(50)     NOT NULL,
   LAST         CHAR(50)     NOT NULL,
   EMAIL        CHAR(50)
);
'''
cursor.execute(sql)
conn.commit()

cursor.execute(
   "INSERT INTO students (STUDENTID,FIRST,LAST,EMAIL) "
   "VALUES (1,'Lauren','Shareshian','lauren@gmail.com');"
)
conn.commit()

cursor.execute("SELECT * FROM students;")
rows = cursor.fetchall()
print(rows)

# close the cursor to avoid memory leaks
cursor.close()

# close the connection to avoid memory leaks
conn.close()