import re
import string
from random import SystemRandom

import pygal
from flask import render_template
from sqlalchemy import desc

from app import db
from app.models import User, Pocket, Transfer, Category
from datetime import datetime, date

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


# - DONE
def validate_email(email):
    pattern = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return (re.search(pattern, email))


# - DONE
def validate_username(username):
    u = User.query.filter_by(username=str(username)).first()
    if u: return False
    return True


# - DONE
def email_exist(email):
    for user in User.query.all():
        if user.email == email: return True
    return False


# - DONE
def user_exist(username):
    for user in User.query.all():
        if user.username == username: return True
    return False


# - DONE
def validate_password(password):
    lowers = '[+a-z]'
    uppers = '[+A-Z]'
    digits = '[+0-9]'
    if re.search(lowers,password) and re.search(uppers,password) and re.search(digits, password) and len(password) >= 8:
        return True
    return False


# - DONE
def validate_loginattempt(data):
    user = User.query.filter_by(username=str(data['username'])).first()
    if not user:
        return False
    if not user.check_password(str(data['password'])):
        return False
    return True


def generate_rnd(N):
    return ''.join(SystemRandom().choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(N))


def generate_vercode(N):
    return ''.join(SystemRandom().choice(string.digits) for _ in range(N))


#sending mail to user
def sendmail(apikey, token, mail, url, uname):   

    #put this into environment variable
    APIKEY = apikey
    link = url + '/rstpwd/' + token

    htm = render_template('resetmail.html', mainpage= url, link= link, username=uname)

    message = Mail(
        from_email= 'blancer.mailing@gmail.com',
        to_emails= mail,
        subject= 'Blancer password reset',
        html_content= htm
    )

    try:
        sg = SendGridAPIClient(APIKEY)
        response = sg.send(message)

    except Exception as e:
        return False

    return True


# - DONE
def rpwd(data, user):
    if not user.check_password(str(data['o_pw'])):
        return 1
    if str(data['n_pw1']) != str(data['n_pw2']):
        return 2
    if not validate_password(str(data['n_pw1'])):
        return 3
    if str(data['o_pw']) == str(data['n_pw1']):
        return 4
    user.set_password(str(data['n_pw1']))
    db.session.commit()
    return 0


# - DONE
def hassu():
    for user in User.query.all():
        if user.is_superuser: return True
    return False


# - DONE!
def verifiy_signup(data):

    if not validate_email(data['email']) or email_exist(data['email']):
        return 1

    if not validate_password(data['password1']):
        return 2

    if data['password1'] != data['password2']:
        return 3

    if not data['agreed']:
        return 4

    if not validate_username(data['username']):
        return 5

    # all data OK, create user and, a default pocket, and two default categories
    u = User()
    u.username = str(data['username'])
    u.set_password(str(data['password1']))
    u.is_superuser = False
    u.email = str(data['email'])
    u.joined = date.today()
    u.last_activity = datetime.now()
    db.session.add(u)

    d_i = Category(name='default income', _user=u, type=1)
    d_i.last_active = datetime.now()
    db.session.add(d_i)
    d_e = Category(name='default expense', _user=u, type=-1)
    d_e.last_active = datetime.now()
    db.session.add(d_e)

    p = Pocket(name='default pocket', _user=u)
    db.session.add(p)

    db.session.commit()

    return 0


# - DONE
def deluser(data):
    u = User.query.get(int(data['userid']))
    if not u : return False
    if not u.is_superuser:
        db.session.delete(u)
        db.session.commit()
        return u.username


def getid(username):
    users = User.query.all()
    for user in users:
        if user.username == username:
            return user.id
    return False


# - DONE
def addpocket(data,u):
    p=Pocket(_user=u )

    p.last_change = datetime.now()

    p.name = str(data['p_name'])

    if data['p_desc'] and data['p_desc'] != '':
        p.description = str(data['p_desc'])
    else:
        p.description = ''

    if data['p_balance'] and data['p_balance'] != '':
        p.balance = int(data['p_balance'])
    else:
        p.balance = 0

    db.session.add(p)
    db.session.commit()
    return True


# - DONE
def delpocket(data):
    p = Pocket.query.get(int(data['p_id']))
    if not p: return False
    db.session.delete(p)
    db.session.commit()
    return True


# - DONE
def delcategory(id):
    c = Category.query.get(int(id))
    c.hidden = True
    db.session.commit()
    return True


# - DONE
def add_cat(data,u):

    if not data['cid']:

        if data['type']:
            t=1
        else:
            t=-1

        cats = Category.query.filter_by(_user=u).filter_by(hidden=False).all()
        for cat in cats:
            if cat.name == str(data['cname']) and cat.type == t:
                return False

        newc = Category(_user=u, name=str(data['cname']), last_active=datetime.now(), type=t)

        db.session.add(newc)
        db.session.commit()
        return True

    else:

        if data['type']:
            t=1
        else:
            t=-1

        newc = Category.query.get(int(data['cid']))

        cats = Category.query.filter_by(_user=u).filter_by(hidden=False).all()
        for cat in cats:
            if cat.name == str(data['cname']) and cat.type == t:
                return False

        newc.name = data['cname']
        if data['type']:
            newc.type = 1
        else:
            newc.type = -1

        db.session.commit()
        return True


# - DONE
def add_transfer(data,u):

    pocket = Pocket.query.get(int(data['pocketid']))
    category = Category.query.get(int(data['categoryid']))
    category.last_active = datetime.now()
    amount = category.type*int(data['amount'])
    detail = str(data['detail'])

    pocket.balance += amount

    transfer = Transfer(amount=amount, _category=category, _pocket=pocket, detail=detail)

    db.session.add(transfer)
    db.session.commit()

    return True


# - DONE
def get_ptransfers(u,num=None):
    #print('positives')
    transfers = {}

    pockets = Pocket.query.filter_by(_user=u).all()
    for pocket in pockets:
        tr_by_pocket = []
        id = pocket.id
        ts=Transfer.query.filter_by(_pocket=pocket).order_by(desc(Transfer.timestamp)).all()
        for transf in ts:
            if transf._category.type == 1:
                tr_by_pocket.append(transf)

        if num:
            transfers[id] = tr_by_pocket[:num]
        else:
            transfers[id] = tr_by_pocket
    #print(transfers)
    return transfers


# - DONE
def get_ntransfers(u,num=None):
    #print('negatives')
    transfers = {}

    pockets = Pocket.query.filter_by(_user=u).all()
    for pocket in pockets:
        tr_by_pocket = []
        id = pocket.id
        ts = Transfer.query.filter_by(_pocket=pocket).order_by(desc(Transfer.timestamp)).all()
        for transf in ts:
            if transf._category.type == -1:
                tr_by_pocket.append(transf)

        if num:
            transfers[id] = tr_by_pocket[:num]
        else:
            transfers[id] = tr_by_pocket

    #print(transfers)
    return transfers


#TODO finish this!
def drawcharts(data):

    fromdate = datetime.fromtimestamp( int(int(data['mintime'])/1000) )
    todate = datetime.fromtimestamp( int(int(data['maxtime'])/1000) )

    fd = datetime(fromdate.year, fromdate.month, fromdate.day)
    td = datetime(todate.year, todate.month, todate.day+1)

    pocket = Pocket.query.get(int(data['pid']))
    transfers = []
    tf = Transfer.query.filter_by(_pocket=pocket).order_by(Transfer.timestamp).all()
    for transfer in tf:
        if td >= transfer.timestamp >= fd:
            transfers.append(transfer)

    charts = []

    charts.append(draw_exp_pie(transfers))
    charts.append(draw_inc_pie(transfers))
    charts.append(draw_multiline(transfers))

    return charts


#- DONE
def draw_exp_pie(data):

    names = []
    amounts = []

    for transfer in data:
        if transfer.amount > 0:
            continue
        else:
            if str(transfer._category.name) not in names:
                names.append(str(transfer._category.name))
                amounts.append(transfer.amount)
            else:
                amounts[names.index( str(transfer._category.name) )] += transfer.amount

    pie_chart = pygal.Pie(inner_radius=.5, width=800, height=400, margin=10, human_readable=True)
    pie_chart.title = 'All expenses'
    for name in names:
        pie_chart.add(name, abs(amounts[names.index(name)]))

    return pie_chart.render_data_uri()


#- DONE
def draw_inc_pie(data):

    names = []
    amounts = []

    for transfer in data:
        if transfer.amount < 0:
            continue
        else:
            if str(transfer._category.name) not in names:
                names.append(str(transfer._category.name))
                amounts.append(transfer.amount)
            else:
                amounts[names.index( str(transfer._category.name) )] += transfer.amount

    pie_chart = pygal.Pie(inner_radius=.5, width=800, height=400, margin=10)
    pie_chart.title = 'All incomes'
    for name in names:
        pie_chart.add(name, abs(amounts[names.index(name)]))

    return pie_chart.render_data_uri()


def draw_multiline(data):

    postransfers = []
    negtransfers =[]

    tdelta = (data[-1].timestamp-data[0].timestamp)

    if tdelta.days <= 0:
        formatter = lambda dt: dt.strftime('%d, %b, %I:%M')
    elif 7 >= tdelta.days > 1:
        formatter = lambda dt: dt.strftime('%d, %b, %I')
    elif 30 >= tdelta.days > 7:
        formatter = lambda dt: dt.strftime('%d, %b %Y')
    else:
        formatter = lambda dt: dt.strftime('%d, %b %Y')



    for transfer in data:

        time = datetime(
            int(transfer.timestamp.strftime('%Y')),
            int(transfer.timestamp.strftime('%m')),
            int(transfer.timestamp.strftime('%d')),
            int(transfer.timestamp.strftime('%I')),
            int(transfer.timestamp.strftime('%M')),
            int(transfer.timestamp.strftime('%S')),
        )

        if transfer.amount > 0:
            postransfers.append( (time,transfer.amount) )
        else:
            negtransfers.append( (time, transfer.amount) )

    r = False

    multiline = pygal.DateTimeLine(
        x_label_rotation=35,
        truncate_label=-1,
        x_value_formatter= formatter,
        width=800,
        height=400,
        margin=10
    )

    multiline.add("Incomes", postransfers)

    multiline.add('Expenses', negtransfers)

    return multiline.render_data_uri()