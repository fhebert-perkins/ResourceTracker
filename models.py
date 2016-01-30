from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    email       = db.Column(db.String(255), unique=True)
    password    = db.Column(db.String(40))
    isAdmin     = db.Column(db.Boolean)

    def __init__(self, email, password, isAdmin=False):
        self.email      = email
        self.password   = bcrypt.generate_password_hash(password)
        self.isAdmin    = isAdmin

    def login(self, password):
        return bcrypt.check_password_hash(self.password, password)
        
    def __repr__(self):
        return "<User %r>" % self.email

class Transaction(db.Model):
    id          = db.Column(db.Integer, primary_key=True) # transaction id
    owner       = db.Column(db.String(128))
    serial      = db.Column(db.String(128))
    model       = db.Column(db.String(128))
    transtype   = db.Column(db.Integer)
    date        = db.Column(db.DateTime)
    notes       = db.Column(db.Text)

    def __init__(self, owner, serial, model, transtype, notes):
        self.owner      = owner
        self.serial     = serial
        self.model      = model
        self.transtype  = transtype
        self.date       = datetime.now()
        self.notes      = notes

    def __repr__(self):
        return "<Transaction %r>" % self.id

class TransactionType(db.Model):
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(40))

    def __init__(self, name):
        self.name       = name
