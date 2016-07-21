from flask import Flask, json
from flask.ext.sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../tmp/database.db'
db = SQLAlchemy(app)


class UserModel(db.Model):
    __tablename__ = 'usermodel'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120))
    deviceid = db.Column(db.String(120))
    cellphone = db.Column(db.String(10))
    admin = db.Column(db.Boolean())
    permuser = db.Column(db.Boolean())
    parentuser = db.Column(db.String(80))
    expirationDate = db.Column(db.String(80))
    weekday = db.relationship('weekDay', cascade='all,delete-orphan', single_parent=True, backref=db.backref('usermodel', lazy='joined'))

    def __init__(self, username, password, deviceid, cellphone, admin, permuser, parentuser, expirationDate):
        self.username = username
        self.password = password
        self.deviceid = deviceid
        self.cellphone = cellphone
        self.admin = admin
        self.permuser = permuser
        self.parentuser = parentuser
        self.expirationDate = expirationDate

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

class WeekdaySchema(Schema):
    id = fields.Int(dump_only=True)
    dayname = fields.Str()
    checked = fields.Boolean()
    allday = fields.Boolean()
    startTime = fields.Str()
    endTime = fields.Str()

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str()
    password = fields.Str()
    admin = fields.Boolean()
    permuser = fields.Boolean()
    parentuser = fields.Str()
    expirationDate = fields.Str()
    weekday = fields.Nested(WeekdaySchema, many=True, only=["dayname","checked","allday","startTime","endTime"])

