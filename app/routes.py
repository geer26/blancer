from flask import render_template, redirect, request
from app import app
from app.forms import LoginForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = LoginForm

    if request.method == 'POST':
        print('what now?')
        if form.validate_on_submit():
            return redirect('/')

    user = {'username': 'geer26'}
    return render_template('index.html', title='Home', user=user)
