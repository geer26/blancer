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
    pockets = db.relationship('Pocket', backref='_user', cascade = 'all,delete')
    categories = db.relationship('Category', backref='_user', cascade = 'all, delete')

    def __repr__(self):
        return self.username

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def compare_passwords(self, password1, password2):
        return generate_password_hash(password1) == generate_password_hash(password2)


class Pocket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(120), default='')
    balance = db.Column(db.Integer, default=0)
    last_change = db.Column(db.DateTime, index=True, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    transfers = db.relationship('Transfer', backref = '_pocket', cascade = 'all,delete')

    def __repr__(self):
        return str(self.id)+'_'+str(self.name)


class Transfer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, default=0)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)
    pocket = db.Column(db.Integer, db.ForeignKey('pocket.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

    def __repr__(self):
        return str(self.id)+'_'+str(self.amount)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    type = db.Column(db.Integer, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # THINK OF CASCADING!!!
    transfer = db.relationship('Transfer', backref='_category')

    def __repr__(self):
        return self.name