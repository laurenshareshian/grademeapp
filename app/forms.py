from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField, IntegerField, FloatField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Email, NumberRange, Length
from wtforms.fields.html5 import DateField
import datetime

class TeacherForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telephone = StringField('Phone', validators=[Length(max=10)])
    submit1 = SubmitField('Submit')

class StudentForm(FlaskForm):
    first_name = StringField('First', validators=[DataRequired()])
    last_name = StringField('Last', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    telephone = StringField('Phone', validators=[Length(max=10)])
    year = IntegerField('Year', validators=[DataRequired()])
    submit1 = SubmitField('Submit')

class AssignmentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    due = DateField("Due", validators=[DataRequired()])
    points = IntegerField('Points', validators=[DataRequired()])
    course = IntegerField('Course')
    submit2 = SubmitField('Submit')

class CourseForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    section = IntegerField('Section', validators=[DataRequired()])
    department = StringField('Department', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    units = FloatField('Units', validators=[DataRequired()])
    teacher = IntegerField('Teacher')
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