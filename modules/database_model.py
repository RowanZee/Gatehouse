from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../tmp/database.db'
db = SQLAlchemy(app)


class UserModel(db.Model):
    __tablename__ = 'usermodel'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120), unique=True)
    admin = db.Column(db.Boolean())
    experationDate = db.Column(db.String(80))
    weekday = db.relationship('weekDay',single_parent=True, backref=db.backref('usermodel', cascade="all, delete-orphan"))

    def __init__(self, username, password, admin, experationDate):
        self.username = username
        self.password = password
        self.admin = admin
        self.experationDate = experationDate

class weekDay(db.Model):
    __tablename__ = 'weekday'
    id = db.Column(db.Integer, primary_key=True)
    #Defining the Foreign Key on the Child Table
    dayname = db.Column(db.String(15))
    checked = db.Column(db.Boolean())
    allday = db.Column(db.Boolean())
    startTime = db.Column(db.String(20))
    endTime = db.Column(db.String(20))
    usermodel_id = db.Column(db.Integer, db.ForeignKey('usermodel.id'))

    def __init__(self, dayname, checked, allday,startTime, endTime):
        self.dayname = dayname
        self.checked = checked
        self.allday = allday
        self.startTime = startTime
        self.endTime = endTime