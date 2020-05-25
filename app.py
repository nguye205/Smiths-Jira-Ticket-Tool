from flask import Flask, session, request, Response, render_template, redirect, url_for
import requests
import itertools
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import Regexp, Optional, InputRequired, Email, Length
from wtforms.fields.html5 import EmailField
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import re
from flask.json import jsonify
from jira import JIRA
from jira.exceptions import JIRAError
from flask_bootstrap import Bootstrap
import sqlite3
from flask_sqlalchemy import SQLAlchemy

user = 'khai.nguyen@smiths-medical.com'
#apikey = 'ipQ24Oe9uE8v2p8zKgHIAB99' #bad
apikey = 'pV8myEaK91Lc5dHsEAbsCB38' #good
newTicket=''

csrf = CSRFProtect()
app = Flask(__name__)
app.config["SECRET_KEY"] = "a chicken has two legs"
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
login_mng = LoginManager(app)
login_mng.login_view = 'login'

class UserAccount(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True)
    password = db.Column(db.String(40))
    api = db.Column(db.String())

class TicketForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    protocol = StringField('Protocol', validators=[InputRequired()])
    srs = StringField('SRS', validators=[InputRequired()])
    testCase = StringField('Test Case', validators=[InputRequired()])
    label = SelectField('Label', choices=[('','-'),('FormalSVT','Formal run'),('DrySVT','Dry run')], validators=[InputRequired()])
    runNumber = SelectField('Pass:', choices=[('','-'),('9','9'),('10','10'),('11','11'),('12','12'),('NA','NA')], validators=[InputRequired()])
    expectedResult = TextAreaField('Expected Result', validators=[InputRequired()])
    actualResult = TextAreaField('Actual Result', validators=[InputRequired()])
    stepsToReproduce = TextAreaField('Steps to reproduce', validators=[InputRequired()])
    pumpSerialNumber = StringField('Pump SN', validators=[InputRequired()])
    pumpType = SelectField('Pump type', choices=[('','-'),('LVP','LVP'),('SYR','SYR')], validators=[InputRequired()])
    library = StringField('Library', validators=[InputRequired()])
    firmwareVersion = StringField('Firmware version', validators=[InputRequired()])
    issue = TextAreaField('Issue', validators=[InputRequired()])
    project = SelectField('Project', choices=[('','-'), ('SAN','SAN'), ('SMPUM','SMPUM')], validators=[InputRequired()])

class LoginForm(FlaskForm):
    email = EmailField('Email Address', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    api = StringField('API key')
    remember_me = BooleanField('Remember me')

@app.route('/success', methods=['POST','GET'])
def success():
    global newTicket
    return render_template("success.html", newTicket=newTicket)

def submitBugTicket(ticketForm):
    Summary = ticketForm.title.data
    Label = ticketForm.label.data + "-" + ticketForm.runNumber.data
    Pump = '*Pump:* ' + ticketForm.pumpSerialNumber.data
    PumpType = ticketForm.pumpType.data
    Library = '*Library:* ' + ticketForm.library.data
    Firmware = '*Firmware:* ' + ticketForm.firmwareVersion.data
    Project = ticketForm.project.data

    #No need to update the rest of these variables
    server = 'https://smithsforge.atlassian.net'
    StepsToReproduce = "*Steps to reproduce:* \n" + ticketForm.stepsToReproduce.data
    IssueDescription = "*Issue:* " + ticketForm.issue.data
    Requirement = "*Requirement:* " + ticketForm.srs.data
    TestProcedure = "*Test Procedure:* "+ ticketForm.protocol.data
    Expected = '*Expected Result:* ' + ticketForm.expectedResult.data
    Actual = '*Actual Result:* ' + ticketForm.actualResult.data
    TestCase = '*Test Case:* ' + ticketForm.testCase.data

    options = {
     'server': server
    }

    global user
    global apikey

    try:
        jira = JIRA(options, basic_auth=(user, apikey))
        jira.create_issue(fields={
            'project': {'key': Project},  #Change SMPUM to SAN for debug/test mode
            'issuetype': {
                "name": "Bug"
            },
            'summary': Summary + " (" + ticketForm.protocol.data + " " +Label+")",
            'description': TestProcedure +"\n" +Requirement + "\n" +TestCase +"\n\n"+ IssueDescription +"\n\n"+ StepsToReproduce +"\n\n" + Expected +"\n\n"+ Actual,
            'labels': [Label],
            'environment': Pump+" ("+PumpType+")"+"\n"+Firmware+ "\n"+Library
        })
    except JIRAError as e:
        if e.status_code == 401:
            print(e)
            return '<h1>Login to JIRA failed. Check your username and API token</h1><a class="nav-link" href="/">Click here to go back</a><br><a class="nav-link" href="https://id.atlassian.com/manage-profile/security/api-tokens">Get new API key</a>'
        if e.status_code == 403:
            print(e)
            return '<h1>You do not have permission to do this</h1><a class="nav-link" href="/">Click here to go back</a>'
        if e.status_code == 400:
            print(e)
            return '<h1>Missing required field or contains invalid field value</h1><a class="nav-link" href="/">Click here to go back</a>'
        else:
            print(e)
            errorCode = '<h1>'+'An error has occurred.'+'\n'+'Error code: '+ str(e.status_code) +'</h1>'
            return errorCode + '<a class="nav-link" href="/">Click here to go back</a>'
    global newTicket
    newTicket =server+"/projects/"+Project+"/issues/?filter=reportedbyme"
    return redirect(url_for('success'))

@app.route('/', methods=['POST','GET'])
def index():
    global user
    global apikey
    ticketForm = TicketForm()
    if ticketForm.validate_on_submit():
        return submitBugTicket(ticketForm)
    return render_template("index.html", ticketForm=ticketForm, user='user' in session, apikey=apikey)

@app.route('/register', methods=['POST','GET'])
def register():
    Loginform = LoginForm()
    if Loginform.validate_on_submit():
        pw_hash = generate_password_hash(Loginform.password.data, method='sha1') # sha1 hashes creates 40 characters
        newUser = UserAccount(username=Loginform.email.data, password=pw_hash, api=Loginform.api.data)
        db.session.add(newUser)
        try:
            db.session.commit()
        except:
            db.session.close()
            return '<h1 style="color: #111;font-size: 25px; font-weight: bold; letter-spacing: -1px; line-height: 1; text-align: center;" > You already have an account! <br><a href="/login">Click here to login</a></h1> '
            #return render_template("login.html", Loginform = Loginform, temp = 1)
        db.session.close()
        return '<h1 style="color: #111;font-size: 25px; font-weight: bold; letter-spacing: -1px; line-height: 1; text-align: center;" > User has been created <br><a href="/login">Click here to login</a></h1> '
    return render_template("register.html", Loginform=Loginform)


@app.route('/login', methods=['POST','GET'])
def login():
    Loginform = LoginForm()
    if Loginform.validate_on_submit():
        print('validate')
        user = UserAccount.query.filter_by(username=Loginform.email.data).first() # only get one result
        if user:        # if user exists, get the Password
            if check_password_hash(user.password, Loginform.password.data):
                login_user(user, remember=Loginform.remember_me.data)
                session['id'] = user.id
                session['user'] = user.username
                print('added to session')
                return redirect(url_for('index'))
        return '<h1 style="color: #111;font-size: 25px; font-weight: bold; letter-spacing: -1px; line-height: 1; text-align: center;" > Username or password does not exist! <br><a href="/login">Click this link to get redirected to the login page </a><br><a href="/register">Click here to register</a></h1> '
    return render_template("login.html", Loginform=Loginform, user='user' in session)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user', None)
    session.pop('id', None)
    return redirect(url_for('index'))
