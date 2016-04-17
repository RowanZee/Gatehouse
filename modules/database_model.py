from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../tmp/database.db'
db = SQLAlchemy(app)


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(120), unique=True)
    admin = db.Column(db.Boolean())
    experationDate = db.Column(db.String(80))
	weekday = db.relationship('weekDays', backref="usermodels", cascade="all, delete-orphan" , lazy='dynamic')


    def __init__(self, username, password, admin, experationDate):
        self.username = username
        self.password = password
        self.admin = admin
        self.experationDate = experationDate


class weekDay(db.Model):
	id=db.Column(dn.Integer, primary_key=True)
	#Defining the Foreign Key on the Child Table
	usermodel_id = db.Column(db.Integer, db.ForeignKey('UserModel.id'))
	
	