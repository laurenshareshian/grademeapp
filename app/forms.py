from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

class ClassesForm(FlaskForm):
    teachername = StringField('', validators=[DataRequired()])
    submit = SubmitField('Search')
    
class StudentForm(FlaskForm):
    first = StringField('First', validators=[DataRequired()])
    last = StringField('Last', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit1 = SubmitField('Submit')
    
class AssignmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    points = StringField('Points', validators=[DataRequired()])
    submit2 = SubmitField('Submit')

class AddCourseForm(FlaskForm):
    courseName = StringField('Course name', validators=[DataRequired()])
    submit1 = SubmitField('Submit')