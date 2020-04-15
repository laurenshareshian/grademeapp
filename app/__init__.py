from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# import the psycopg2 database adapter for PostgreSQL
from psycopg2 import connect, extensions, sql

from urllib.parse import urlparse
#result = urlparse("postgresql://objectrocket:mypass@localhost/postgres")
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




# # declare a new PostgreSQL connection object
# conn = connect(
# dbname = "postgres",
# user = "objectrocket",
# host = "localhost",
# password = "mypass"
# )

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



from app import routes, models