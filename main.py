from flask import Flask, flash, request, redirect, render_template, url_for
from models.Forms import LoginForm

app = Flask(__name__)

# config app
app.config['SECRET_KEY'] = 'SECRET_KEY'

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    if request.method == 'POST' and login_form.validate_on_submit():
        password = login_form.password.data
        print('Password:', password)
        if password == 'S&Lrail8':
            flash('Login Successful!')
            return redirect(url_for('database'))
        else:
            flash('Login Unsuccessful. Please try again.')

    return render_template('login.html', login_form=login_form)

@app.route('/database')
def database():
    return render_template('database.html')

if __name__ == '__main__':
    app.run(debug=True)