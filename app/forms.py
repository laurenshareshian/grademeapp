from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField, IntegerField, SelectField, SelectMultipleField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, NumberRange
import datetime

class TeacherForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    telephone = StringField('Phone', validators=[DataRequired()])
    submit1 = SubmitField('Submit')

class StudentForm(FlaskForm):
    first_name = StringField('First', validators=[DataRequired()])
    last_name = StringField('Last', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    telephone = StringField('Phone', validators=[DataRequired()])
    year = StringField('Year', validators=[DataRequired()])
    submit1 = SubmitField('Submit')

class AssignmentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    due = StringField('Due', validators=[DataRequired()])
    points = StringField('Points', validators=[DataRequired()])
    course = IntegerField('Course')
    submit2 = SubmitField('Submit')

class CourseForm(FlaskForm):
    title = StringField('Course title', validators=[DataRequired()])
    section = StringField('Section', validators=[DataRequired()])
    department = StringField('Department', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    units = StringField('Units', validators=[DataRequired()])
    teacher = SelectField('Teacher')
    submit1 = SubmitField('Submit')

class SubmissionForm(FlaskForm):
    sub_time = DateTimeField(
        label='Submission date and time',
        format='%Y-%m-%d %H:%M:%S',
        validators=[DataRequired('Enter a date')]
    )
    grade = IntegerField('Grade', validators=[DataRequired(), NumberRange(0, 100)])
    assignment = SelectField('Assignment')
    students = SelectMultipleField('Students', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.sub_time.data:
            self.sub_time.data = datetime.datetime.now()