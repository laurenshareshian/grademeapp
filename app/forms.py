from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

class TeacherForm(FlaskForm):
    first = StringField('First name', validators=[DataRequired()])
    last = StringField('Last name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    submit1 = SubmitField('Submit')
    
class StudentForm(FlaskForm):
    first = StringField('First', validators=[DataRequired()])
    last = StringField('Last', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    year = StringField('Year', validators=[DataRequired()])
    submit1 = SubmitField('Submit')
    
class AssignmentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    due = StringField('Due', validators=[DataRequired()])
    points = StringField('Points', validators=[DataRequired()])
    submit2 = SubmitField('Submit')

class CourseForm(FlaskForm):
    title = StringField('Course title', validators=[DataRequired()])
    section = StringField('Section', validators=[DataRequired()])
    department = StringField('Department', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    units = StringField('Units', validators=[DataRequired()])
    submit1 = SubmitField('Submit')