from datetime import date, datetime

from flask import render_template, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, socket, db
from app.forms import LoginForm, SignupForm
from app.models import User
from workers import verify_login, verifiy_signup, hassu


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    loginform = LoginForm()
    signupform = SignupForm()

    if request.method == 'POST' and not current_user.is_authenticated:
        if loginform.validate_on_submit():
            user = User.query.filter_by(username=loginform.username.data).first()
            if user is None or not user.check_password(loginform.password.data):
                #SHOW ERROR!
                return redirect('/')

            login_user(user, remember=loginform.remember_me.data)
            user.last_activity = datetime.now()
            db.session.commit()
            return redirect('/')

    if current_user.is_authenticated and current_user.is_superuser:
        users = User.query.all()
        return render_template('index.html', title='SU index', loginform=loginform, signupform=signupform, users=users)
    elif current_user.is_authenticated and not current_user.is_superuser:
        return render_template('index.html', title='Index', loginform=loginform, signupform=signupform)
    else:
        return render_template('index.html', title='Index', loginform=loginform, signupform=signupform)


@app.route('/logout')
@login_required
def logout():
    user = current_user
    user.last_activity = datetime.now()
    db.session.commit()
    logout_user()
    return redirect('/')


@app.route('/addsu/<suname>/<password>')
def addsu(suname, password):
    #eg. https://example.com/examplesuname/example1Password!2
    if not hassu():
        user = User()
        user.username = suname
        user.email = 'none@none.no'
        user.set_password(password)
        user.is_superuser = True
        user.joined = date.today()
        user.avatar = '/static/img/avatars/adminavatar.png'
        db.session.add(user)
        db.session.commit()
    return redirect('/')


'''
@app.route('/bfrb')
@login_required
def bfrb():  #swipe database!
    if current_user.is_superuser:
        #del all users
        users = User.query.all()
        for user in users:
            if not user.is_superuser:
                db.session.delete(user)
                db.session.commit()
        #del all messages
        messages = Message.query.all()
        for message in messages:
            db.session.delete(message)
            db.session.commit()


@app.route('/clear_messages')
@login_required
def clear_messages():  #swipe messages!
    if current_user.is_superuser:
        #del all messages
        messages = Message.query.all()
        for message in messages:
            db.session.delete(message)
            db.session.commit()
    return redirect('/')
'''


@socket.on('newmessage')
def newmessage(data):

    #print(data)

    sid = request.sid

    # incoming login request
    if data['event'] == 221:
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

        return True

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


