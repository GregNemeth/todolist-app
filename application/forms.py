from flask_wtf import FlaskForm
from wtforms.fields.core import StringField
from wtforms.fields.simple import SubmitField

class TaskForm(FlaskForm):
    name = StringField('What to do?')
    submit = SubmitField('Submit')