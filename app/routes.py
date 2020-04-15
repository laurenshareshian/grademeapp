from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm
from psycopg2 import connect, extensions, sql

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
    # connect to the new database
    conn = connect(
        dbname="grades",
        user="objectrocket",
        host="localhost",
        password="mypsword"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students;")
    names = cursor.fetchall()
    print(names)
    return render_template('testsql.html', names=names)