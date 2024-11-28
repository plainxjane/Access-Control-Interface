from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SelectMultipleField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Optional, ValidationError
from wtforms import validators
from wtforms.widgets import ListWidget, CheckboxInput


class LoginForm(FlaskForm):
    password = PasswordField('Password')
    submit = SubmitField('Submit')


class AddLayerForm(FlaskForm):
    name = StringField('Name')
    department = SelectMultipleField('Department to add layer to', choices=[],
                                     widget=ListWidget(prefix_label=False),
                                     option_widget=CheckboxInput(), )

    groups = SelectMultipleField('Group to add layer to', choices=[],
                                 widget=ListWidget(prefix_label=False),
                                 option_widget=CheckboxInput(),
                                 )
    submit = SubmitField('Submit')


class AddUserForm(FlaskForm):
    name = StringField('Name')
    department = SelectMultipleField("Choose user's department", choices=[],
                                     widget=ListWidget(prefix_label=False),
                                     option_widget=CheckboxInput())
    group = SelectMultipleField("Choose user's group", choices=[],
                                widget=ListWidget(prefix_label=False),
                                option_widget=CheckboxInput())
    editor = SelectMultipleField('Editor', choices=[],
                                 widget=ListWidget(prefix_label=False),
                                 option_widget=CheckboxInput(), )
    viewer = SelectMultipleField('Viewer', choices=[],
                                 widget=ListWidget(prefix_label=False),
                                 option_widget=CheckboxInput(), )
    download_attachments = SelectMultipleField('Download Attachments', choices=[],
                                               widget=ListWidget(prefix_label=False),
                                               option_widget=CheckboxInput(), )
    submit = SubmitField('Submit')


class UpdateUserForm(FlaskForm):
    pass
