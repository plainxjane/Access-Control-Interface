from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SelectMultipleField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Optional, ValidationError
from wtforms import validators
from wtforms.widgets import ListWidget, CheckboxInput


class LoginForm(FlaskForm):
    password = PasswordField('Password')
    submit = SubmitField('Submit')


class AddLayerForm(FlaskForm):
    name = StringField('Name of layer')
    group = SelectMultipleField('Select group to add layer to', choices=[('IDE General Viewers', 'IDE General Viewers'),
                                                                         ('Editors_ARCH', 'Editors_ARCH'),
                                                                         ('Editors_CRI', 'Editors_CRI'),
                                                                         ('Editors_CSV', 'Editors_CSV'),
                                                                         ('Editors_CTIPS', 'Editors_CTIPS'),
                                                                         ('Editors_GTT', 'Editors_GTT'),
                                                                         ('Editors_LAND', 'Editors_LAND')],
                                widget=ListWidget(prefix_label=False),
                                option_widget=CheckboxInput(),
                                )
    submit = SubmitField('Submit')


class AddUserForm(FlaskForm):
    pass


class UpdateUserForm(FlaskForm):
    pass
