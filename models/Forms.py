from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SelectMultipleField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Optional, ValidationError
from wtforms import validators
from wtforms.widgets import ListWidget, CheckboxInput
import sqlite3

DATABASE = 'database.db'


class LoginForm(FlaskForm):
    password = PasswordField('Password')
    submit = SubmitField('Submit')


def fetch_choices(table_name):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # fetch data from the specified table
    cursor.execute(f'SELECT name FROM {table_name}')
    choices = [(row[0], row[0]) for row in cursor.fetchall()]

    return choices


class AddLayerForm(FlaskForm):
    # dynamically populate choices for Departments & Groups
    departments = fetch_choices('departments')
    groups = fetch_choices('groups')

    name = StringField('Name')
    department = SelectMultipleField('Department to add layer to', choices=departments,
                                     widget=ListWidget(prefix_label=False),
                                     option_widget=CheckboxInput(),
                                     )

    groups = SelectMultipleField('Group to add layer to', choices=groups,
                                 widget=ListWidget(prefix_label=False),
                                 option_widget=CheckboxInput(),
                                 )
    submit = SubmitField('Submit')


class AddUserForm(FlaskForm):
    # dynamically populate choices for Departments & Groups
    departments = fetch_choices('departments')
    groups = fetch_choices('groups')
    layers = fetch_choices('layers')

    name = StringField('Name')
    department = SelectMultipleField("Choose user's department", choices=departments,
                                     widget=ListWidget(prefix_label=False),
                                     option_widget=CheckboxInput())
    groups = SelectMultipleField("Choose user's group", choices=groups,
                                widget=ListWidget(prefix_label=False),
                                option_widget=CheckboxInput())
    editor = SelectMultipleField('Editor', choices=layers,
                                 widget=ListWidget(prefix_label=False),
                                 option_widget=CheckboxInput(), )
    viewer = SelectMultipleField('Viewer', choices=layers,
                                 widget=ListWidget(prefix_label=False),
                                 option_widget=CheckboxInput(), )
    download_attachments = SelectMultipleField('Download Attachments', choices=layers,
                                               widget=ListWidget(prefix_label=False),
                                               option_widget=CheckboxInput(), )
    submit = SubmitField('Submit')


class UpdateUserForm(FlaskForm):
    pass
