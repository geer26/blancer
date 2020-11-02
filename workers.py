import re

from app import app,socket,db
from app.models import User, Pocket, Transfer, Category
from datetime import datetime, date


# - DONE
def validate_email(email):
    pattern = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    return (re.search(pattern, email))


# - DONE
def email_exist(email):
    for user in User.query.all():
        if user.email == email: return True

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
def hassu():
    for user in User.query.all():
        if user.is_superuser: return True
    return False


# - NEEDS TEST
def verifiy_signup(data):

    if not validate_email(data['email']) or email_exist(data['email']):
        return 1

    if not validate_password(data['password1']):
        return 2

    if data['password1'] != data['password2']:
        return 3

    if not data['agreed']:
        return 4

    # all data OK, create user and, a default pocket, and two default categories
    u = User()
    u.username = data['username']
    u.set_password(str(data['password1']))
    u.is_superuser = False
    u.email = data['email']
    u.joined = date.today()
    u.last_activity = datetime.now()
    db.session.add(u)

    d_i = Category(name='default income', _user=u, type=1)
    db.session.add(d_i)
    d_e = Category(name='default expense', _user=u, type=-1)
    db.session.add(d_e)

    p = Pocket(name='default', _user=u)
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
    db.session.delete(c)
    db.session.commit()
    return True


# - DONE
def add_cat(data,u):
    if data['cid']:
        c=Category.query.get(int(data['cid']))
        c.name=data['cname']
        if data['type']:
            c.type = 1
        else:
            c.type = -1
    else:
        c = Category(name=data['cname'], _user=u)
        if data['type']:
            c.type = 1
        else:
            c.type = -1
        db.session.add(c)
    db.session.commit()
    return True


# - DONE
def add_transfer(data,u):
    pocket = Pocket.query.get(int(data['pocketid']))
    category = Category.query.get(int(data['categoryid']))
    amount = category.type*int(data['amount'])

    pocket.balance += amount

    transfer = Transfer(amount=amount, _category=category, _pocket=pocket)

    db.session.add(transfer)
    db.session.commit()

    return True
