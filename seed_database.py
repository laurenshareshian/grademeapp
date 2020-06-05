import time
from psycopg2.extras import execute_values

def seed(cursor):
  seed_student(cursor)
  seed_teacher(cursor)
  seed_course(cursor)
  seed_assignment(cursor)
  seed_submission(cursor)
  seed_student_submission(cursor)
  seed_student_course(cursor)


def seed_student(cursor):
  execute_values(cursor,
    "INSERT INTO student (first_name, last_name, year, email, telephone) VALUES %s",
    [
      ('Kanye', 'West', 2020, 'kanye@gmail.com', '6094397996'),
      ('Anthony', 'Fauci', 2021, 'fauci@gmail.com', '5555555555'),
      ('Tiger', 'King', 2021, 'iluvtigers@gmail.com', '5555555555'),
      ('Lion', 'King', 2021, 'iluvlionss@gmail.com', '5555555555'),
      ('Charles', 'Lindberg', 1922, 'wheresmykid@now.huh', '5555555555'),
      ('Amelia', 'Earhart', 1931, 'mapsareforwimps@oce.an', '5555555555'),
      ('Howard', 'Hughes', 1928, 'luvgoose@how.hu', '5555555555'),
      ('Bessie', 'Coleman', 1905, 'suckitchumps@up.here', '5555555555'),
      ('Glenn', 'Curtiss', 1911, 'needmoredanger@me.now', '5555555555')
    ]
  )


def seed_teacher(cursor):
  execute_values(cursor,
    "INSERT INTO teacher (first_name, last_name, email, telephone) VALUES %s",
    [
      ('Lauren','Shareshian','lauren@gmail.com', '6094397996'),
      ('Joshua','Cox','cox@gmail.com', '5555555555'),
      ('Elon','Musk Baby','baby@gmail.com', '5555555555'),
      ('5G','Conspiracy Theorist','5G@gmail.com', '5555555555'),
      ('Dante','Aligheri','florencesux@gmail.com', '5555555555'),
      ('Sea','Biscuit','getoffmyback@gmail.com', '5555555555')
    ]
  )


def seed_course(cursor):
  execute_values(cursor,
    "INSERT INTO course (title, section, department, description, units, teacher) VALUES %s",
    [
      ('Calculus', '100', 'Math', 'Integrals', 4, 1),
      ('Basketweaving', '400', 'Art', 'Weaving stuff', 3, 2),
      ('Algebra', '100', 'Math', 'Functions', 3, 1),
      ('Advanced Tickling', '100', 'HR Problems', 'Creepy stuff', 5, None),
      ('Expensive Remote Learning Course', '100', 'Science', 'same price as an in-person class without any labs', 5, 3),
      ('Electricity', '100', 'Science', 'electricity stuff', 5, 4),
      ('Principles of Eating', '101', 'Food', 'Chewing and swallowing', 5, 5),
      ('Analysis of Toast', '505', 'Food', 'The rise and fall of hot bread in society', 3, 5),
      ('Milk', '403', 'Food', 'Tolerating intolerance', 5, 5),
      ('Confusion', '202', 'Philosophy', 'Utilizing uncertainty and stupidity', 4, 6),
      ('Trotting', '103', 'Physical Education', 'Techniques and survey of graceful stomping', 1, 6)
    ]
  )


def seed_assignment(cursor):
  execute_values(cursor,
    "INSERT INTO assignment (title, description, due, points, course) VALUES %s",
    [
      ('HW 1', 'Book exercises', '2020-01-01', 5, 1),
      ('Group Project', 'Derivatives', '2020-01-02', 50, 1),
      ('Exam 1', 'Slope', '2020-01-02', 50, 3),
      ('Basket 1', 'basket', '2020-01-02', 100, 2),
      ('Foot tickle', 'tickle', '2020-01-02', 100, 4),
      ('HW Exercises', 'chapter 1', '2020-01-02', 100, 6),
      ('Chewing', 'Vertical motion', '2020-01-02', 80, 7),
      ('Rye', 'Color and odor', '2020-01-02', 100, 8),
      ('Confuse a cat', 'Stun and alarm', '2020-01-02', 100, 9),
      ('Basic steps', 'Swing those hoofs', '2020-01-02', 50, 10),
    ]
  )


def seed_submission(cursor):
  datetime_now = time.strftime('%Y-%m-%d %H:%M:%S')

  execute_values(cursor,
    "INSERT INTO submission (submitted, grade, assignment) VALUES %s",
    [
      (datetime_now, 55, 1),
      (datetime_now, 72, 1),
      (datetime_now, 90, 2),
      (datetime_now, 60, 3)
    ]
  )


def seed_student_submission(cursor):
  execute_values(cursor,
    "INSERT into student_submission (student_id, submission_id) VALUES %s",
    [
      (1, 2),
      (1, 3),
      (2, 1),
      (2, 4),
      (1, 5),
      (3, 3),
    ]
  )


def seed_student_course(cursor):
  execute_values(cursor,
    "INSERT into student_course (student_id, course_id) VALUES %s",
    [
      (1, 1),
      (1, 2),
      (1, 3),
      (2, 1),
      (3, 1),
      (2, 3),
      (3, 5),
      (5, 7),
      (6, 10),
      (7, 8),
      (8, 9),
      (9, 9),
    ]
  )
