from app import app
from psycopg2 import pool
from urllib.parse import urlparse

result = urlparse(app.config['DATABASE_URL'])

username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname
port = result.port

db_pool = pool.ThreadedConnectionPool(
    1,
    20,
    database=database,
    user=username,
    password=password,
    host=hostname,
    port=port
)