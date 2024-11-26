from flask import Flask, flash, request, redirect, render_template, url_for
from models.Forms import LoginForm, AddLayerForm, AddUserForm, UpdateUserForm

app = Flask(__name__)

# config app
app.config['SECRET_KEY'] = 'SECRET_KEY'


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
        group = add_layer_form.group.data

        print("Layer added successfully!")

    return render_template('add_layer.html', form=add_layer_form)


@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
    pass


@app.route('/update_user', methods=['POST', 'GET'])
def update_user():
    pass


@app.route('/database')
def database():
    return render_template('database.html')


if __name__ == '__main__':
    app.run(debug=True)
