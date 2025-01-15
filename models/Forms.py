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
    # dynamically populate choices for Departments & Groups from sqlite database
    departments = fetch_choices('departments')
    groups = fetch_choices('groups')

    name = StringField('Name')
    department = SelectMultipleField('Department', choices=departments, coerce=str,
                                     widget=ListWidget(prefix_label=False),
                                     option_widget=CheckboxInput(),
                                     )

    groups = SelectMultipleField('Group', choices=groups, coerce=str,
                                 widget=ListWidget(prefix_label=False),
                                 option_widget=CheckboxInput(),
                                 )
    submit = SubmitField('Submit')


class UpdateLayerForm(FlaskForm):
    # dynamically populate choices for Departments & Groups from sqlite database
    departments = fetch_choices('departments')
    groups = fetch_choices('groups')

    name = StringField('Name')
    department = SelectMultipleField('Department', choices=departments, coerce=str,
                                     widget=ListWidget(prefix_label=False),
                                     option_widget=CheckboxInput(),
                                     )

    groups = SelectMultipleField('Group', choices=groups, coerce=str,
                                 widget=ListWidget(prefix_label=False),
                                 option_widget=CheckboxInput(),
                                 )
    submit = SubmitField('Submit')


class AddUserForm(FlaskForm):
    # dynamically populate choices for Departments, Groups & Layers from sqlite database
    departments = fetch_choices('departments')
    groups = fetch_choices('groups')
    layers = fetch_choices('layers')

    name = StringField('Name')
    department = SelectMultipleField('Department', choices=departments, coerce=str,
                                     widget=ListWidget(prefix_label=False),
                                     option_widget=CheckboxInput(), )
    groups = SelectMultipleField('Group', choices=groups, coerce=str,
                                widget=ListWidget(prefix_label=False),
                                option_widget=CheckboxInput(), )
    editor = SelectMultipleField('Editor', choices=layers, coerce=str,
                                 widget=ListWidget(prefix_label=False),
                                 option_widget=CheckboxInput(), )
    viewer = SelectMultipleField('Viewer', choices=layers, coerce=str,
                                 widget=ListWidget(prefix_label=False),
                                 option_widget=CheckboxInput(), )
    submit = SubmitField('Submit')


class UpdateUserForm(FlaskForm):
    # dynamically populate choices for Departments, Groups & Layers from sqlite database
    departments = fetch_choices('departments')
    groups = fetch_choices('groups')
    layers = fetch_choices('layers')

    name = StringField('Name')
    department = SelectMultipleField('Department', choices=departments, coerce=str,
                                     widget=ListWidget(prefix_label=False),
                                     option_widget=CheckboxInput(),)
    groups = SelectMultipleField('Group', choices=groups, coerce=str,
                                 widget=ListWidget(prefix_label=False),
                                 option_widget=CheckboxInput(), )
    editor = SelectMultipleField('Editor', choices=layers, coerce=str,
                                 widget=ListWidget(prefix_label=False),
                                 option_widget=CheckboxInput(), )
    viewer = SelectMultipleField('Viewer', choices=layers, coerce=str,
                                 widget=ListWidget(prefix_label=False),
                                 option_widget=CheckboxInput(), )
    submit = SubmitField('Submit')


class AddDepartmentForm(FlaskForm):
    name = StringField('Department Name:')
    submit = SubmitField('Submit')


class AddGroupForm(FlaskForm):
    name = StringField('Group Name:')
    submit = SubmitField('Submit')


class AddDashboardForm(FlaskForm):
    # dynamically populate choices for Departments & Groups from sqlite database
    departments = fetch_choices('departments')
    groups = fetch_choices('groups')

    name = StringField('Name')
    department = SelectMultipleField('Department', choices=departments, coerce=str,
                                     widget=ListWidget(prefix_label=False),
                                     option_widget=CheckboxInput(),
                                     )

    groups = SelectMultipleField('Group', choices=groups, coerce=str,
                                 widget=ListWidget(prefix_label=False),
                                 option_widget=CheckboxInput(),
                                 )
    submit = SubmitField('Submit')
