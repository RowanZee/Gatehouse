from flask import Flask, json
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../tmp/database.db'
db = SQLAlchemy(app)


class UserModel(db.Model):
    __tablename__ = 'usermodel'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))
    admin = db.Column(db.Boolean())
    permuser = db.Column(db.Boolean())
    parentuser = db.Column(db.String(80))
    expirationDate = db.Column(db.String(80))
    weekday = db.relationship('weekDay', cascade='all,delete-orphan', single_parent=True, backref=db.backref('usermodel', lazy='joined'))

    def __init__(self, username, password, admin, permuser, parentuser, expirationDate):
        self.username = username
        self.password = password
        self.admin = admin
        self.permuser = permuser
        self.parentuser = parentuser
        self.expirationDate = expirationDate

    def reprJSON(self):
        return dict(username=self.username, password=self.password, admin=self.admin, permuser=self.permuser, parentuser=self.parentuser, expirationDate=self.expirationDate) 


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

    def reprJSON(self):
        return dict(dayname=self.dayname, checked=self.checked, allday=self.allday, startime=self.startTime, endtime=self.endTime) 

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj,'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)