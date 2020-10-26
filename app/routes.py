from datetime import date, datetime

from flask import render_template, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from app import app, socket, db
from app.forms import LoginForm, SignupForm
from app.models import User, Pocket
from workers import verify_login, verifiy_signup, hassu, deluser, getid, addpocket, delpocket


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    loginform = LoginForm()
    signupform = SignupForm()

    if request.method == 'POST' and not current_user.is_authenticated:

        if loginform.validate_on_submit():
            user = User.query.filter_by(username=loginform.username.data).first()

            if not user or not user.check_password(loginform.password.data):
                mess = {}
                mess['event'] = 191
                mess['htm'] = render_template('errormessage.html', message='Incorrect password or username')
                socket.emit('newmessage', mess)

            elif user and user.check_password(loginform.password.data):
                login_user(user, remember=loginform.remember_me.data)
                user.last_activity = datetime.now()
                db.session.commit()
                return redirect('/')

    if current_user.is_authenticated and current_user.is_superuser:
        users = User.query.all()
        pockets = Pocket.query.all()
        return render_template('index.html', title='SU index', loginform=loginform, signupform=signupform, users=users, pockets=pockets)

    elif current_user.is_authenticated and not current_user.is_superuser:
        pockets = Pocket.query.filter_by( user_id = current_user.id ).all()
        return render_template('index.html', title='Index', loginform=loginform, signupform=signupform, pockets=pockets)

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


@app.route('/del_users')
@login_required
def del_users():  #swipe database!
    if current_user.is_superuser:
        #del all users
        users = User.query.all()
        for user in users:

            if not user.is_superuser:
                db.session.delete(user)
                db.session.commit()

        return redirect('/')


@app.route('/del_pockets')
@login_required
def del_pockets():  #swipe database!
    if current_user.is_superuser:
        #del all users
        pockets = Pocket.query.all()
        for pocket in pockets:
            db.session.delete(pocket)
            db.session.commit()
        return redirect('/')


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


    #delete username
    if data['event'] == 271:
        if current_user.is_superuser:

            mess = {}
            mess['event'] = 171
            mess['to_del'] = deluser(data)
            socket.emit('newmessage', mess, room=sid)

            pockets = Pocket.query.filter_by(user_id=int(data['userid'])).all()
            mess = {}
            mess['event'] = 171
            for pocket in pockets:
                mess['to_del'] = pocket.id
                socket.emit('newmessage', mess, room=sid)
        return True


    #user want to add a pocket
    if data['event'] == 241 and current_user.is_authenticated:
        mess = {}
        mess['event'] = 141
        mess['htm'] = render_template('addpocket_modal.html')
        socket.emit('newmessage', mess, room=sid)


    #user want to del a pocket
    if data['event'] == 242 and current_user.is_authenticated:
        mess = {}
        mess['event'] = 142
        mess['htm'] = render_template('delpocket_confirm.html', p_id=data['p_id'])
        socket.emit('newmessage', mess, room=sid)


    #user send a new pocket data
    if data['event'] == 243 and current_user.is_authenticated:
        if addpocket(data,current_user):

            pockets = Pocket.query.filter_by(user_id=current_user.id).all()

            mess = {}
            mess['event'] = 148
            mess['status'] = 1
            mess['htm'] = render_template('usercarousel.html', pockets=pockets)
            socket.emit('newmessage', mess, room=sid)
        return True


    #user confirms to delete a pocket
    if data['event'] == 244 and current_user.is_authenticated:

        if delpocket(data):
            mess = {}
            mess['event'] = 149
            mess['status'] = 1
            mess['pid'] = 'uc_'+str(data['p_id'])
            socket.emit('newmessage', mess, room=sid)
        return True

