import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField,BooleanField,SubmitField,IntegerField
from wtforms.validators import AnyOf, DataRequired, Length, NumberRange, Regexp, URL, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_sqlalchemy import SQLAlchemy
from wtforms.fields.html5 import TelField
from wtforms.widgets.html5 import NumberInput, TelInput
from flask_wtf.recaptcha import widgets

class MovieForm(FlaskForm):
    title = StringField(
        'title', validators=[DataRequired()]
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired(),Regexp('(\d{4})-(\d{2})-(\d{2}) (\d{2}):(\d{2}):(\d{2})')],
        default= datetime.datetime.now(),
        # render_kw={'disabled':''}
    )    
    submit = SubmitField('Save')

class ActorForm(FlaskForm):
    
    name = StringField(
        'name', validators=[DataRequired()]
    )
    age = IntegerField(
        'age', validators=[DataRequired()]
    )
    gender = SelectField(
        'gender', validators=[DataRequired()],
        choices=[
            ('Female', 'Female'),
            ('Male', 'Male'),
            ('Other','Other')
        ]
    )
    submit = SubmitField('Save')    
