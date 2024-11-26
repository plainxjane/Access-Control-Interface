from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Optional,ValidationError
from wtforms import validators

class LoginForm(FlaskForm):
    password = PasswordField('Password')
    submit = SubmitField('Submit')