import re

from pygal.style import DarkSolarizedStyle, CleanStyle

from app import app,socket,db
from app.models import User, Pocket, Transfer
from datetime import datetime, date, timedelta

import random
from random import randrange

import pygal


def tranfers_by_dates(startdate, days, tf):
    transfers = {}
    min = []
    plu = []

    d = startdate - timedelta(days)

    for t in tf:
        if t['timestamp'] >= d:
            if t['value'] <= 0:
                min.append(t)
            else:
                plu.append(t)

    transfers['minus'] = min
    transfers['plus'] = plu

    #print(transfers)

    return transfers


def pygaltest(u):
    charts = {}
    id = u.id
    transferlist = []
    transfers = {}

    # get pockets related to current user
    pockets = Pocket.query.filter_by(user_id=id).all()

    # iter over the pockets
    for p in pockets:

        # get transfers related to pocket
        trfs = Transfer.query.filter_by(pocket=p.id).all()

        # iter over the transfers
        for tr in trfs:
            transfer = {}
            # create dict from transfer
            transfer['timestamp'] = tr.timestamp
            transfer['current_balance'] = tr.cba
            transfer['id'] = tr.id
            transfer['value'] = tr.t_type*tr.amount

            # add current transfer dict to transferlist
            transferlist.append(transfer)

        #get transfers by days back
        #tranfers_by_dates(datetime.now(), 213, transferlist)

        one_year = tranfers_by_dates(datetime.now(), 365, transferlist)
        yearly_in = []
        yearly_exp = []
        yearly_balance = []
        for income in one_year['plus']:
            yearly_in.append(income['value'])
            yearly_balance.append(income['current_balance'])
        for expense in one_year['minus']:
            yearly_exp.append(expense['value'])
            yearly_balance.append(expense['current_balance'])

        # add all transfers related to pocket
        transfers[p.id] = transferlist

        # create yearly chart from transfers
        transfers_yearly = pygal.Line(
            height=200,
            width=600,
            is_unicode=True,
            interpolate='cubic',
            fill = False,
            style=CleanStyle,
        )

        transfers_yearly.title = 'yearly sum of ' + str(p.name)
        transfers_yearly.x_labels = map(str, range(12, 0))
        transfers_yearly.add('Income', yearly_in)
        transfers_yearly.add('Expense', yearly_exp)
        #transfers_yearly.add('Balance', yearly_balance)

        # add all transfers related to pocket
        charts[str(p.id)+'_year'] = transfers_yearly

    return charts


def validate_email(email):
    pattern = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return (re.search(pattern, email))


def email_exist(email):
    for user in User.query.all():
        if user.email == email: return True

    return False


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

    if not validate_email(data['email']) or email_exist(data['email']):
        return 1

    if not validate_password(data['password1']):
        return 2

    if data['password1'] != data['password2']:
        return 3

    if not data['agreed']:
        return 4

    u = User()
    u.username = data['username']
    u.set_password(str(data['password1']))
    u.is_superuser = False
    u.email = data['email']
    u.joined = date.today()
    u.last_activity = datetime.now()
    db.session.add(u)
    p = Pocket(name='default', user=u)
    db.session.add(p)

    db.session.commit()

    return 0


def verify_login(data):
    uname = str(data['username'])
    user = User.query.filter_by(username=uname).first()
    if user and user.check_password(data['password']):
        return True
    else:
        return False


def errormessage(data):
    pass


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


def addpocket(data,u):
    p=Pocket(user=u)

    p.name = data['p_name']

    if data['p_desc'] and data['p_desc'] != '':
        p.description = data['p_desc']
    else:
        p.description = 'none'

    if data['p_balance'] and data['p_balance'] != '':
        p.balance = int(data['p_balance'])
    else:
        p.balance = 0

    db.session.add(p)
    db.session.commit()
    return True


def delpocket(data):
    p = Pocket.query.get(int(data['p_id']))
    if not p: return False
    db.session.delete(p)
    db.session.commit()
    return True


def random_date(start, end):
    """
    This function will return a random datetime between two datetime
    objects.
    """
    start = datetime(start[0], start[1], start[2], 0, 0, 0)
    end = datetime(end[0], end[1], end[2], 23, 59, 59)

    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return (start + timedelta(seconds=random_second))


def generate(iters=100, amount=[1000, 15000], poc=1):

    p = Pocket.query.get(int(poc))
    actual_balance = p.balance

    for i in range(iters):
        tr = Transfer()

        r = {}
        types = [-1, 1]
        r['type'] = random.choice(types)
        r['amount'] = randrange(amount[0], amount[1] + 1)
        r['timestamp'] = random_date([2018, 2, 3], [2020, 10, 24])
        r['pocket'] = int(poc)

        actual_balance = r['type']*r['amount']

        tr.pocket = int(poc)
        tr.amount = r['amount']
        tr.t_type = r['type']
        tr.timestamp = r['timestamp']
        tr.cba = actual_balance

        db.session.add(tr)

    p.balance =actual_balance
    db.session.commit()

    return True