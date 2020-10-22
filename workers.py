import re

from app import app,socket,db
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from datetime import datetime, date, timedelta


def validate_email(email):
    pattern = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return (re.search(pattern, email))


def validate_password(password):
    lowers = '[+a-z]'
    uppers = '[+A-Z]'
    digits = '[+0-9]'
    if re.search(lowers,password) and re.search(uppers,password) and re.search(digits, password) and len(password) >= 8:
        return True
    return False


def hassu():
    for user in User.query.all():
        if user.is_superuser: return True
    return False


def verifiy_signup(data):
    #print(data)
    #print(date.today())
    # print(db.__sizeof__()) <- useful for check the database size

    #first check values
    #if error:
    # message = {}
    #message['event'] = 191
    #socket.emit('newmessage', message,  room=data['sid'])
    #return False
    #else

    u = User()
    u.username = data['username']
    u.set_password(str(data['password1']))
    u.is_superuser = False
    u.email = data['email']
    u.joined = date.today()
    db.session.add(u)
    db.session.commit()

    return True


def verify_login(data):
    uname = str(data['username'])
    user = User.query.filter_by(username=uname).first()
    if user and user.check_password(data['password']):
        #login_user(user, remember=data['remember'])
        #print('logged_in')
        return True
    else:
        return False


def errormessage(data):
    pass