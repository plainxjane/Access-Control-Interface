from flask import Flask, g, flash, request, redirect, render_template, url_for
from models.Forms import LoginForm, AddLayerForm, AddUserForm, UpdateUserForm
from collections import defaultdict
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

# config app
app.config['SECRET_KEY'] = 'SECRET_KEY'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.route('/')
def home():
    return render_template('homepage.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    if request.method == 'POST' and login_form.validate_on_submit():
        password = login_form.password.data
        if password == 'S&Lrail8':
            flash('Login Successful!')
            return redirect(url_for('database'))
        else:
            flash('Login Unsuccessful. Please try again.')

    return render_template('login.html', form=login_form)


@app.route('/add_layer', methods=['POST', 'GET'])
def add_layer():
    add_layer_form = AddLayerForm()

    if request.method == 'POST' and add_layer_form.validate_on_submit():
        # process the form data
        name = add_layer_form.name.data
        departments = add_layer_form.department.data
        groups = add_layer_form.groups.data

        # convert lists into comma-separated strings
        department_string = ', '.join(departments)
        group_string = ', '.join(groups)

        # insert into SQLite database
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            cursor.execute('''
            INSERT INTO layers (name, department, groups)
            VALUES (?, ?, ?)
            ''', (name, department_string, group_string))

            conn.commit()
            conn.close()

            print("Layer added successfully!")
            return redirect(url_for('all_layers'))

        except sqlite3.Error as e:
            print(f"An error: {e}")

    else:
        return render_template('add_layer.html', form=add_layer_form)


@app.route('/layers')
def all_layers():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM layers')
    rows = cursor.fetchall()

    return render_template('layers.html', rows=rows)


@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
    add_user_form = AddUserForm()

    if request.method == 'POST' and add_user_form.validate_on_submit():
        name = add_user_form.name.data
        departments = add_user_form.department.data
        groups = add_user_form.groups.data
        editor = add_user_form.editor.data
        viewer = add_user_form.viewer.data
        download_attachments = add_user_form.download_attachments.data

        # convert lists into comma-separated strings
        department_string = ', '.join(departments)
        group_string = ', '.join(groups)
        editor_string = ', '.join(editor)
        viewer_string = ', '.join(viewer)
        download_attachments_string = ', '.join(download_attachments)

        # insert into SQLite database
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            cursor.execute('''
                    INSERT INTO users (name, department, groups, editor, viewer, download_attachments)
                    VALUES (?, ?, ?, ?, ?, ?)
                    ''', (
            name, department_string, group_string, editor_string, viewer_string, download_attachments_string))

            conn.commit()
            conn.close()

            print("User added successfully!")
            return redirect(url_for('users'))

        except sqlite3.Error as e:
            print(f"An error: {e}")

    else:
        return render_template('add_user.html', form=add_user_form)


@app.route('/update_user/<int:user_id>', methods=['POST', 'GET'])
def update_user(user_id):
    # fetch user's data from database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?",
                   (user_id,))
    user_data = cursor.fetchone()
    conn.close()

    if not user_data:
        print("User not found!")
        return redirect(url_for('users'))

    # create & populate the form
    update_user_form = UpdateUserForm(name=user_data[1], department=user_data[2].split(', '),
                                      groups=user_data[3].split(', '), editor=user_data[4].split(', '),
                                      viewer=user_data[5].split(', '),
                                      download_attachments=user_data[6].split(', '))

    # update the user's information in database
    if request.method == 'POST' and update_user_form.validate_on_submit():
        updated_name = update_user_form.name.data
        updated_department = ', '.join(update_user_form.department.data)
        updated_groups = ', '.join(update_user_form.groups.data)
        updated_editor = ', '.join(update_user_form.editor.data)
        updated_viewer = ', '.join(update_user_form.viewer.data)
        updated_download_attachments = ', '.join(update_user_form.download_attachments.data)

        # update SQLite database
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('''
            UPDATE users
            SET name = ?, department = ?, groups = ?, editor = ?, viewer = ?, download_attachments = ?
            WHERE id = ?
            ''', (
                updated_name, updated_department, updated_groups, updated_editor, updated_viewer,
                updated_download_attachments,
                user_id))

            conn.commit()
            conn.close()

            return redirect(url_for('all_users'))

        except sqlite3.Error as e:
            print(f"An error occurred: {e}", "error")

    return render_template('update_user.html', form=update_user_form)


@app.route('/users')
def all_users():
    db = get_db()
    cursor = db.cursor()

    #fetch users
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    # fetch layers
    cursor.execute('SELECT name, department FROM layers')
    layers = cursor.fetchall()

    # fetch departments
    cursor.execute('SELECT name FROM departments')
    departments = [dept[0] for dept in cursor.fetchall()]

    # split user fields before passing to template
    split_users = []
    for user in users:
        split_users.append({
            'id': user[0],
            'name': user[1],
            'department': user[2].split(', '),
            'groups': user[3].split(', '),
            'editor': user[4].split(', '),
            'viewer': user[5].split(', '),
            'download_attachments': user[6].split(', '),
        })

    return render_template('users.html', users=split_users, layers=layers, departments=departments)


@app.route('/database')
def database():
    return render_template('database.html')


if __name__ == '__main__':
    app.run(debug=True)
