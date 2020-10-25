from datetime import datetime

from app import login

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import db


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin,db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(12), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(256))
    is_superuser = db.Column(db.Boolean, default=False)
    joined = db.Column(db.Date)
    last_activity = db.Column(db.DateTime)
    avatar = db.Column(db.String(128), default='/static/img/avatars/a_unknown.png')

    def __repr__(self):
        return self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def compare_passwords(self, password1, password2):
        #print( generate_password_hash(password1) == generate_password_hash(password2) )
        return generate_password_hash(password1) == generate_password_hash(password2)


class Pocket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(120), default='')
    balance = db.Column(db.Integer, default=0)
    last_change = db.Column(db.DateTime, index=True, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return self.balance


class Transfer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    t_type = db.Column(db.Integer, default=1)
    amount = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    pocket = db.Column(db.Integer, db.ForeignKey('pocket.id'))
    category = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __repr__(self):
        return self.t_type*self.amount


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return self.name