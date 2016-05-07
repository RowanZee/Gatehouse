# IMPORTS
from flask import Flask, request, redirect, url_for, \
    render_template
import random

# MODULES
from modules.security import Security
from modules.user import User
from modules.database import Database
from modules.garage import Garage
from modules.settings import Settings
from collections import namedtuple
from datetime import date


# GLOBAL VARIABES
DEBUG = True  # This needs to be commented out in master for security.

# Master login
settings = Settings()
USERNAME = settings.username()
PASSWORD = settings.password()

# Secret Key for sessions
SECRET_KEY = str(random.random())

# Init App
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./tmp/database.db'


@app.route('/', methods=['GET'])
# GET - Shows main page
# POST - None
def index():
    if not user.loggedIn():
        return redirect(url_for('login'))
    else:
        return render_template('index.html')


@app.route('/login/', methods=['GET', 'POST'])
# GET - Shows login page
# POST - Logs user in
def login():
    # Redirects on GET request
    if request.method == 'GET':
        return render_template('login.html')

    # Gets login info from page
    username = request.form['username']
    password = request.form['password']

    # fetches user from database
    databaseUser = database.getUser(username)
    if databaseUser:
        # Checks username and password against the database
        if (username == databaseUser.username and
                security.encrypt(password) == databaseUser.password):
            # Checks if user is temporary and if the date is expired
            if (databaseUser.experationDate != 'False' and
                    user.isExpired(databaseUser.experationDate)):
                # Returns expired message
                error = "Your temporary account has expired."
                return render_template('login.html', error=error)

            # Logs user in
            user.login()
            user.setName(username)
            # Checks if user is admin
            if databaseUser.admin is True:
                # Sets admin status
                user.setAdmin()
            # Returns Index
            return redirect(url_for('index'))

    # Checks if master user
    if (request.form['username'] == app.config['USERNAME'] and
       request.form['password'] == app.config['PASSWORD']):
            # Logs user in
            user.login()
            user.setName(request.form['username'])
            # Sets admin status
            user.setAdmin()
            # Returns Index
            return redirect(url_for('index'))

    # Returns invalid login message
    error = "Invalid Username or Password."
    return render_template('login.html', error=error, username=username)


@app.route('/logout/', methods=['GET'])
# GET - Logs user out
# POST - None
def logout():
    # Logs user out
    user.logout()
    # Returns index
    return redirect(url_for('index'))


@app.route('/users/', methods=['GET', 'POST'])
# GET - Shows user creation and lists users
# POST - Creates Users
def users():
    # Checks if logged in
    if not user.loggedIn():
        # Returns logged in if not
        return redirect(url_for('login'))

    # Checks if admin
    if not user.isAdmin():
        # Returns index if not
        return redirect(url_for('index'))

    # Checks if GET request
    if request.method == 'GET':
        # Returns users and success message if available
        success = request.args.get('success')
        return render_template('users.html', users=database.userList(),
                               success=success)

    # Get username from page
    username = request.form['username']
    # Gets user from database
    databaseUser = database.getUser(username)
    # Checks if user exists
    if (databaseUser is not None):
        # Returns error message
        error = "User already exists"
        return render_template('users.html', users=database.userList(),
                               error=error)

    # Checks if username is valid
    if (not security.usernameStrength(username)):
        error = "Username must be at least 3 characters long"
        return render_template('users.html', users=database.userList(),
                               error=error)

    # Get password from page
    password = request.form['password']
    # Checks if password is valid
    if security.passwordStrength(password) is True:
        # Encrypts password
        password = security.encrypt(password)
    else:
        # Returns invalid password
        error = "Your password must be at least 6 characters long and\
                 contain a number"
        return render_template('users.html', users=database.userList(),
                               error=error, username=username)

    # Checks if admin is checked
    if request.form.get('adminuser'):
        # A checkbox does not return true or false, so we set it here
        isAdmin = True
    else:
        isAdmin = False

    # Checks if temp user is checked
    if request.form.get('tempuser'):
        # Sets experation date from page
        experationDate = str(request.form.get('dateTmp'))
    else:
        experationDate = 'False'

    #check Monday details
    daycheckname = 'moncheck'
    alldayactive = 'monallday'
    fromdaytime = 'montimefrom'
    todaytime = 'montimeto'
    mondayInfo = getweekday(daycheckname, alldayactive, fromdaytime, todaytime)
    #Tuesday details
    daycheckname = 'tuecheck'
    alldayactive = 'tueallday'
    fromdaytime = 'tuetimefrom'
    todaytime = 'tuetimeto'
    tuesdayInfo = getweekday(daycheckname, alldayactive, fromdaytime, todaytime)
    #Wednesday details
    daycheckname = 'wedcheck'
    alldayactive = 'wedallday'
    fromdaytime = 'wedtimefrom'
    todaytime = 'wedtimeto'
    wednesdayInfo = getweekday(daycheckname, alldayactive, fromdaytime, todaytime)
    #Thursday details
    daycheckname = 'thucheck'
    alldayactive = 'thuallday'
    fromdaytime = 'thutimefrom'
    todaytime = 'thutimeto'
    thursdayInfo = getweekday(daycheckname, alldayactive, fromdaytime, todaytime)
    #Friday details
    daycheckname = 'fricheck'
    alldayactive = 'friallday'
    fromdaytime = 'fritimefrom'
    todaytime = 'fritimeto'
    fridayInfo = getweekday(daycheckname, alldayactive, fromdaytime, todaytime)
    #Saturday details
    daycheckname = 'satcheck'
    alldayactive = 'satallday'
    fromdaytime = 'sattimefrom'
    todaytime = 'sattimeto'
    saturdayInfo = getweekday(daycheckname, alldayactive, fromdaytime, todaytime)
    #Sunday details
    daycheckname = 'suncheck'
    alldayactive = 'sunallday'
    fromdaytime = 'suntimefrom'
    todaytime = 'suntimeto'
    sundayInfo = getweekday(daycheckname, alldayactive, fromdaytime, todaytime)

    # create days
    monday = database.createDay('Monday', mondayInfo.isactive, mondayInfo.isalldayactive, mondayInfo.fromtime, mondayInfo.totime)
    tuesday = database.createDay('Tuesday', tuesdayInfo.isactive, tuesdayInfo.isalldayactive, tuesdayInfo.fromtime, tuesdayInfo.totime)
    wednesday = database.createDay('Wednesday', wednesdayInfo.isactive, wednesdayInfo.isalldayactive, wednesdayInfo.fromtime, wednesdayInfo.totime)
    thursday = database.createDay('Thursday', thursdayInfo.isactive, thursdayInfo.isalldayactive, thursdayInfo.fromtime, thursdayInfo.totime)
    friday = database.createDay('Friday', fridayInfo.isactive, fridayInfo.isalldayactive, fridayInfo.fromtime, fridayInfo.totime)
    saturday = database.createDay('Saturday', saturdayInfo.isactive, saturdayInfo.isalldayactive, saturdayInfo.fromtime, saturdayInfo.totime)
    sunday = database.createDay('Sunday', sundayInfo.isactive, sundayInfo.isalldayactive, sundayInfo.fromtime, sundayInfo.totime)

    # Creates user - add in check for false return
    database.createNewUser(username, password, isAdmin, experationDate, monday, tuesday, wednesday, thursday, friday, saturday, sunday)

    # Returns success message
    success = ("%s was created!")
    success = success % username
    return render_template('users.html', users=database.userList(),
                           success=success)

def getweekday(dayActive, alldayActive, timefrom, timeto):
    dayinfo = namedtuple("info", ["isactive", "isalldayactive", "fromtime", "totime"])
    # Check if the day is active
    if request.form.get(dayActive):
        dayactive = True
    else:
        dayactive = False
    # Check if all day is active
    if request.form.get(alldayActive):
        activeallday = True
    else:
        activeallday = False
    fromTime = request.form.get(timefrom)
    toTime = request.form.get(timeto)
    return dayinfo(dayactive, activeallday, fromTime, toTime)

@app.route('/edituser/', methods=['POST'])
# GET - None
# POST - Edits User
def edituser():
    # Checks if the user is logged in
    if not user.loggedIn():
        return redirect(url_for('login'))

    # Checks if the user is an admin
    if not user.isAdmin():
        return redirect(url_for('index'))

    # Get ID and Username
    userID = request.args.get('userID')

    # Checks if username already exists
    username = request.form['username']

    # Gets user from the database
    databaseUser = database.getUser(username)

    # Checks if username already exists
    if (databaseUser is not None):
        # Returns username error message
        error = "User already exists"
        return render_template('users.html', users=database.userList(),
                               error=error)

    # Gets password from the page, already checked in javascript so no
    # checking needs to happen here.
    if request.form['password']:
        # Encrpys the password
        password = security.encrypt(request.form['password'])
    else:
        password = None

    # Checks admin status
    if (request.form.get('adminuser')):
        isAdmin = True
    else:
        isAdmin = False

    # Gets temp checkbox status from page
    tmpStatus = request.form.get('dateTmp')

    # Checks if temp is checked
    if (tmpStatus):
        # Sets experation date
        experationDate = str(tmpStatus)
    else:
        # Uses string for jinja template (May be able to use actual False)
        experationDate = 'False'

    # Edits user, returns true if success
    if database.editUser(userID, username, password, isAdmin, experationDate):

        # Sends success message
        success = 'User Updated!'
        return redirect(url_for('users', success=success))
    else:
        # Sends error message
        error = 'An error has occured.'
        return redirect(url_for('users', error=error))


@app.route('/removeuser/', methods=['POST'])
# GET - None
# POST - Removes the user
def removeuser():
    # Checks if user is logged in
    if not user.loggedIn():
        return redirect(url_for('login'))

    # Checks if user is admin
    if not user.isAdmin():
        return redirect(url_for('index'))

    # Gets user to remove from json object
    userID = request.json['userID']

    # Removes user, returns a message to page if sucessfull
    if database.removeUser(userID):
        return 'success'
    else:
        return 'fail'


@app.route('/toggledoor/', methods=['POST'])
# GET - None
# POST - Toggles the status of the door
def toggledoor():
    # Checks if user is logged in
    if not user.loggedIn():
        return redirect(url_for('login'))

    if user.isAdmin():
        return redirect(url_for('index', error="ADMIN"))

    username = user.getName()
    isUserAuthorised = authoriseUser(username)
    #verifieduser = verifyUser(username)
    if isUserAuthorised:
        #toggle gate
        return redirect(url_for('index', error="auth"))
    else:
        return redirect(url_for('index', error="HELLO"))

    # Toggles Door
    #garage.toggleDoor()

    # Reloads index
    return redirect(url_for('index'))

def authoriseUser(user):
# fetches user from database
    #databaseUser = database.getUser(user)

    today_weekday = date.today().weekday()

    #Check for day of week   ["isactive", "isalldayactive", "fromtime", "totime"])
    #Monday
    if today_weekday == 0:
        weekday = database.getUserDay(user, "Monday") 
    #Tuesday
    elif today_weekday == 1:
        weekday = database.getUserDay(user, "Tuesday") 
    #Wednesday
    elif today_weekday == 2:
        weekday = database.getUserDay(user, "Wednesday") 
    #Thursday
    elif today_weekday == 3:
        weekday = database.getUserDay(user, "Thursday") 
    #Friday
    elif today_weekday == 4:
        weekday = database.getUserDay(user, "Friday") 
    #Saturday
    elif today_weekday == 5:
        weekday = database.getUserDay(user, "Saturday") 
    #Sunday
    elif today_weekday == 6:
        weekday = database.getUserDay(user, "Sunday") 
    else:
        return False
        #something went wrong

    if weekday.isactive:
        if not weekday.isalldayactive:
            #if the weekday isnt allday active check for times\
            authorised = False
        else:
            authorised = True
    else:
        authorised = False

    return authorised


# INIT the application
if __name__ == "__main__":
    # Class Instances
    security = Security()
    user = User()
    database = Database()
    garage = Garage()

    # Do Stuff
    garage.cleanupRelay()

    # Start The App
    settings = Settings()
    garage.cleanupRelay()
    app.run(host=settings.ipAddress())
