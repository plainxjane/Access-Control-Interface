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


@app.route('/add_layer', methods=['POST', 'GET'])
def add_layer():
    add_layer_form = AddLayerForm()
    if request.method == 'POST' and add_layer_form.validate_on_submit():
        name = add_layer_form.name.data
        department = ', '.join(add_layer_form.department.data)      # convert python list into comma-separated string
        groups = ', '.join(add_layer_form.groups.data)              # convert python list into comma-separated string

        # insert into SQLite database
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()

            cursor.execute('''
            INSERT INTO layers (name, department, groups)
            VALUES (?, ?, ?)
            ''', (name, department, groups))

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


@app.route('/users')
def users():
    return render_template('users.html')


@app.route('/database')
def database():
    return render_template('database.html')


if __name__ == '__main__':
    app.run(debug=True)
