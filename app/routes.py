from flask import render_template, redirect, request
from flask_login import current_user, login_user, logout_user
from app import app, socket
from app.forms import LoginForm, SignupForm
from app.models import User
from workers import verify_login, verifiy_signup


@app.route('/')
@app.route('/index')
def index():

    loginform = LoginForm()
    signupform = SignupForm()

    return render_template('index.html', title='Index', loginform=loginform, signupform=signupform)


@app.route('/login', methods=['POST'])
def login():
    print(request.form)
    user = User.query.filter_by(username=request.form['username']).first()
    if user.check_password(request.form['password']):
        if request.form['remember_me']:
            login_user(user, remember=True)
        else:
            login_user(user)
        # socket.emit('newmessage', {'event': 122})
    return redirect('/')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')


@socket.on('newmessage')
def newmessage(data):

    #print(data)

    sid = request.sid

    # incoming login request
    '''if data['event'] == 221:
        if verify_login(data):
            mess = {}
            mess['event'] = 121
            mess['status'] = 1
            socket.emit('newmessage', mess, room=sid)
        else:
            socket.emit('newmessage', {'event': 129}, room=sid)
            mess = {}
            mess['event'] = 191
            mess['htm'] = render_template('errormessage.html', message='LOGIN NOT SUCCESS!')
            socket.emit('newmessage', mess, room=sid)

        return True'''

    #incoming request for error message with message
    if data['event'] == 291:
        mess = {}
        mess['event'] = 191
        mess['htm'] = render_template('errormessage.html', message=data['message'])
        socket.emit('newmessage', mess, room=sid)


    # incoming signup request
    if data['event'] == 211:
        #"i want to signup with theese data"

        r = verifiy_signup(data)

        if r == 0:
            #ok, data are great, i added you to the database, log in
            mess = {}
            mess['event'] = 111
            mess['htm'] = render_template('infomessage.html', message='You can login now!')
            socket.emit('newmessage', mess, room=sid)

        elif r == 1:
            #invalid email address
            socket.emit('newmessage', {'event': 119}, room=sid)
            mess = {}
            mess['event'] = 191
            mess['htm'] = render_template('errormessage.html', message='Invalid email or email is already registered!')
            socket.emit('newmessage', mess, room=sid)

        elif r == 2:
            # invalid  password
            socket.emit('newmessage', {'event': 119}, room=sid)
            mess = {}
            mess['event'] = 191
            mess['htm'] = render_template('errormessage.html', message='Passord must have UPPER and lowercase chars, numbers, and must be at least 8 chars length!')
            socket.emit('newmessage', mess, room=sid)

        elif r == 3:
            # passwords do not match
            socket.emit('newmessage', {'event': 119}, room=sid)
            mess = {}
            mess['event'] = 191
            mess['htm'] = render_template('errormessage.html', message='Passwords do not match')
            socket.emit('newmessage', mess, room=sid)

        elif r == 4:
            # did not agree
            socket.emit('newmessage', {'event': 119}, room=sid)
            mess = {}
            mess['event'] = 191
            mess['htm'] = render_template('errormessage.html', message='Please read and accept the terms')
            socket.emit('newmessage', mess, room=sid)

        else:
            # no, noo, something isn't ok
            socket.emit('newmessage', {'event': 119}, room=sid)
            mess = {}
            mess['event'] = 191
            mess['htm'] = render_template('errormessage.html', message='SIGNUP NOT SUCCESS!')
            socket.emit('newmessage', mess, room=sid)

        return True


    return True