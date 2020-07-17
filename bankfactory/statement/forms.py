from flask_wtf import FlaskForm
from wtforms import SubmitField,RadioField,SelectField
from wtforms.validators import DataRequired,Email,EqualTo,Length
from flask_wtf.file import FileAllowed
from wtforms.fields.html5 import DateField



class GetStatement(FlaskForm):
    from_date = DateField('From')
    to_date = DateField('To')
    
    period1 = [('Last One Week','Last One Week'),('Last One Month','Last One Month'),('Last One Year','Last One Year')]
    period = SelectField('For',choices=period1)
    
    submit = SubmitField('Get Mini Statement')