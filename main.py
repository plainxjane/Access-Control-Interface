from flask import Flask, g, flash, request, redirect, render_template, url_for
from models.Forms import LoginForm, AddLayerForm, AddUserForm, UpdateUserForm
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


@app.route('/add_departments_groups', methods=['POST', 'GET'])
def add_departments_groups():
    pass


@app.route('/add_layer', methods=['POST', 'GET'])
def add_layer():
    add_layer_form = AddLayerForm()

    # fetch existing departments & groups from database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # fetch unique departments
    cursor.execute('SELECT DISTINCT department from layers')
    departments = [row[0] for row in cursor.fetchall()]

    # fetch unique groups
    cursor.execute('SELECT DISTINCT groups from layers')
    groups = [row[0] for row in cursor.fetchall()]

    conn.close()

    # populate dropdowns with existing departments & groups + 'Add New'
    add_layer_form.department.choices = [(d,d) for d in departments] + [('Add New', 'Add New Department')]
    add_layer_form.groups.choices = [(g, g) for g in groups] + [('Add New', 'Add New Group')]

    if request.method == 'POST' and add_layer_form.validate_on_submit():
        name = add_layer_form.name.data
        selected_department = add_layer_form.department.data
        selected_groups = add_layer_form.groups.data

        # 'Add New' for departments
        if 'Add New' in selected_department:
            new_department = request.form.get('new_department', '').strip()
            if new_department:
                selected_department.remove("Add New")
                selected_department.append(new_department)

        # 'Add New' for groups
        if 'Add New' in selected_groups:
            new_group = request.form.get('new_group', '').strip()
            if new_group:
                selected_groups.remove("Add New")
                selected_groups.append(new_group)

        # convert selected lists into comma-separated strings
        department_string = ', '.join(selected_department)
        group_string = ', '.join(selected_groups)

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
            return redirect(url_for('layers'))

        except sqlite3.Error as e:
            print(f"An error: {e}")

    else:
        return render_template('add_layer.html', form=add_layer_form)


@app.route('/layers')
def layers():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM layers')
    rows = cursor.fetchall()
    print(rows)
    return render_template('layers.html', rows=rows)


@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
    add_user_form = AddUserForm()

    # query layers in database
    db = get_db()
    cursor = db.cursor()
    query = ' SELECT id, name FROM layers '
    cursor.execute(query)
    layers = cursor.fetchall()

    # populate the form choices with the layers in database
    add_user_form.editor.choices = [str(layer[1]) for layer in layers ]
    add_user_form.viewer.choices = [str(layer[1]) for layer in layers ]
    add_user_form.download_attachments.choices = [str(layer[1]) for layer in layers ]

    if request.method == 'POST' and add_user_form.validate_on_submit():
        name = add_user_form.name.data
        editor = add_user_form.editor.data
        viewer = add_user_form.viewer.data
        download_attachments = add_user_form.download_attachments.data

        return redirect(url_for('layers'))

    else:
        return render_template('add_user.html', form=add_user_form)


@app.route('/update_user', methods=['POST', 'GET'])
def update_user():
    pass


@app.route('/user_management')
def users():
    return render_template('users.html')


@app.route('/database')
def database():
    return render_template('database.html')


if __name__ == '__main__':
    app.run(debug=True)
