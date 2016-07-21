from modules.database_model import db
from modules.database_model import UserModel
from modules.database_model import weekDay
from modules.database_model import WeekdaySchema, UserSchema
from collections import namedtuple
import os


class Database:
    def __init__(self):
        # Checks if database exists and creates it if it doest
        directory = './tmp'
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(directory + "/database.db", "a+") as f:
            if f:
                pass
            else:
                pass

        db.create_all()

    # CREATE USER
    def createUser(self, username, password, admin, permuser, parentuser, expirationDate):
        try:
            newUser = UserModel(username, password, admin, permuser, parentuser, expirationDate)
            db.session.add(newUser)
            db.session.commit()
            return True
        except:
            return False

    # CREATE NEW USER
    def createNewUser(self, username, password, admin, permuser, parentuser, expirationDate, day1, day2, day3, day4, day5, day6, day7):
        try:
            newUser = UserModel(username, password, admin, permuser, parentuser, expirationDate)
            newUser.weekday = [day1, day2, day3, day4, day5, day6, day7]
            db.session.add(newUser)
            db.session.commit()
            return True
        except:
            print("Error creating new user")
            db.session.rollback()
            return False

    # Create week day
    def createDay(self, dayname, dayactive, allday, starttime, endtime):
        try:
            newDay = weekDay(dayname, dayactive, allday, starttime, endtime)
            return newDay
        except:
            dprint("Error creating Day")
            return None

    #Create day otherwise Default it if failed
    def createDayorDefault(self, dayname, dayactive, allday, starttime, endtime):
        try:
            newDay = self.createDay(dayname, dayactive, allday, starttime, endtime)
            if (newDay == None):
                newDay = createday(dayname, False, False, 0,0)
            return newDay
        except:
            print("Error creating default Day")
            return None

    # EDIT USER
    def editUser(self, userID, username, password, admin, expirationDate):
        try:
            user = self.getUser(None, userID)
            if username:
                user.username = username
            if password:
                user.password = password
            if expirationDate is not user.expirationDate:
                user.expirationDate = expirationDate

            user.admin = admin
            db.session.commit()
            return True
        except:
            return False

    def removeUser(self, userID):
        try:
            user = self.getUser(None, userID)
            db.session.delete(user)
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    # GET USER
    def getUser(self, username=None, userID=None):
        if username:
            user = UserModel.query.filter_by(username=username).first()
        elif userID:
            user = UserModel.query.filter_by(id=userID).first()
        else:
            user = None
        return user

    # LIST USERS
    def userList(self):
        users = UserModel.query.all()
        return users
 
    # LIST DAYS FOR USER
    def getUserDay(self, userName, dayOfWeek):
        weekdayinfo = namedtuple("weekdayinfo", ["isactive", "isalldayactive", "fromtime", "totime"])
        week_day = weekDay.query.select_from(UserModel).join(UserModel.weekday).filter(UserModel.username == userName).filter(weekDay.dayname==dayOfWeek).first()
        return weekdayinfo(week_day.checked, week_day.allday, week_day.startTime, week_day.endTime)

    def getallUsers(self, userName, admin=False):
        if admin:
            return UserModel.query.all()
        else:
            userlist = UserModel.query.filter_by(parentuser=userName).all()
            full_schema = UserSchema(many=True, exclude=('password','admin','permuser','parentuser', ))
            result, errors = full_schema.dump(userlist)
            return result

    def updateUser(self, userID, username, password, expirationDate):
        try:
            user = self.getUser(None, userID)
            if expirationDate is not user.expirationDate:
                user.expirationDate = expirationDate
            db.session.commit()
            return True
        except:
            return False

    # GET USER DEVICE ID
    def getUserDevice(self, username=None, userID=None):
        if username:
            user = UserModel.query.filter_by(username=username).first()
        elif userID:
            user = UserModel.query.filter_by(id=userID).first()
        else:
            user = None
        return user.deviceid