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
        department = add_layer_form.department.data
        group = add_layer_form.group.data

        print("Layer added successfully!")

    return render_template('add_layer.html', form=add_layer_form)


@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
    add_user_form = AddUserForm()

    return render_template('add_user.html', form=add_user_form)


@app.route('/update_user', methods=['POST', 'GET'])
def update_user():
    pass


@app.route('/database')
def database():
    return render_template('database.html')


@app.route('/layers')
def layers():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM layers')
    rows = cursor.fetchall()
    print(rows)
    return render_template('layers.html', rows=rows)


if __name__ == '__main__':
    app.run(debug=True)
