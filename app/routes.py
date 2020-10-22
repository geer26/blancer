from flask import render_template, redirect, request
from flask_login import current_user, login_user, logout_user
from app import app, socket
from app.forms import LoginForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    loginform = LoginForm()

    if request.method == 'POST':
        print('what now?')

    return render_template('index.html', title='Index', loginform=loginform)

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')