from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm
from psycopg2 import connect, extensions, sql

from urllib.parse import urlparse

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)

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