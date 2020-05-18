from flask import Flask, session, request, Response, render_template, redirect, url_for
import requests
import itertools
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import Regexp, Optional, InputRequired, Email, Length
import re
from flask.json import jsonify
from jira import JIRA
from jira.exceptions import JIRAError
from flask_bootstrap import Bootstrap


user = 'khai.nguyen@smiths-medical.com'
#apikey = 'ipQ24Oe9uE8v2p8zKgHIAB99' #bad
apikey = 'pV8myEaK91Lc5dHsEAbsCB38' #good


csrf = CSRFProtect()
app = Flask(__name__)
app.config["SECRET_KEY"] = "a chicken has two legs"
bootstrap = Bootstrap(app)

class TicketForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()])
    protocol = StringField('Protocol', validators=[InputRequired()])
    srs = StringField('SRS', validators=[InputRequired()])
    label = SelectField('Label', choices=[('','-'),('FormalSVT','Formal run'),('DrySVT','Dry run')], validators=[InputRequired()])
    runNumber = SelectField('Pass:', choices=[('','-'),('9','9'),('10','10'),('11','11'),('12','12'),('NA','NA')], validators=[InputRequired()])
    expectedResult = TextAreaField('Expected Result', validators=[InputRequired()])
    actualResult = TextAreaField('Actual Result', validators=[InputRequired()])
    stepsToReproduce = TextAreaField('Steps to reproduce', validators=[InputRequired()])
    pumpSerialNumber = StringField('Pump serial number', validators=[InputRequired()])
    library = StringField('Library', validators=[InputRequired()])
    firmwareVersion = StringField('Firmware version', validators=[InputRequired()])
    others = TextAreaField('Issue description', validators=[InputRequired()])
    project = SelectField('Project', choices=[('','-'), ('SAN','SAN'), ('SMPUM','SMPUM')], validators=[InputRequired()])
class LoginForm(FlaskForm):
    username = StringField('Smiths email address', validators=[InputRequired()])
    apikey = PasswordField('API Token', validators=[InputRequired()])
    rememberme = BooleanField('Remember me')

def submitBugTicket(ticketForm):
    Summary = ticketForm.title.data
    SSTP = ticketForm.protocol.data
    SRS = ticketForm.srs.data
    Label = ticketForm.label.data + "-" + ticketForm.runNumber.data
    Expected = ticketForm.expectedResult.data
    Actual = ticketForm.actualResult.data
    stepsToReproduce = ticketForm.stepsToReproduce.data
    Pump = ticketForm.pumpSerialNumber.data
    Library = ticketForm.library.data
    Firmware = ticketForm.firmwareVersion.data
    Others = ticketForm.others.data
    Project = ticketForm.project.data

    #No need to update the rest of these variables
    server = 'https://smithsforge.atlassian.net'
    StepsToReproduce = "*Steps to reproduce:* \n" + stepsToReproduce
    IssueDescription = "*Issue description:* " + Others
    Requirement = "*Requirement:* " + SRS
    TestProcedure = "*Test Procedure:* "+ SSTP
    Expected = '*Expected Result:* ' + Expected
    Actual = '*Actual Result:* ' + Actual

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
            'summary': Summary + " (" + SSTP + " " +Label+")",
            'description': TestProcedure +"\n" +Requirement +"\n\n"+ IssueDescription +"\n\n"+ StepsToReproduce +"\n\n" + Expected +"\n\n"+ Actual,
            'labels': [Label],
            'environment': "*Pump:* "+Pump+"\n*Firmware:* "+Firmware+ "\n*Library:* "+Library,

        })
    except JIRAError as e:
        if e.status_code == 401:
            print(e)
            return '<h1>Login to JIRA failed. Check your username and password</h1><a class="nav-link" href="/">Click here to go back</a>'
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

    newTicket ="https://smithsforge.atlassian.net/projects/"+Project+"/issues/?filter=reportedbyme"
    return '<h1>This is your new ticket: <a class="nav-link" href='+newTicket+'>NEW TICKET</a></h1><a class="nav-link" href="/">Click here to go back</a>'

@app.route('/', methods=['POST','GET'])
def index():
    ticketForm = TicketForm()
    if ticketForm.validate_on_submit():
        return submitBugTicket(ticketForm)
    return render_template("index.html", ticketForm=ticketForm)

@app.route('/login.html', methods=['POST','GET'])
def login():
    Loginform = LoginForm()

    if Loginform.validate_on_submit():
        login_user(user, remember=Loginform.rememberme.data)
        session['id'] = user.id
        session['user'] = user.username
        return redirect(url_for('index'))
        #return '<h1>Username or password does not exist</h1> <a href="/">GO TO HOME </a>'# if user doesn't exist
        return '<h1 style="color: #111;font-size: 25px; font-weight: bold; letter-spacing: -1px; line-height: 1; text-align: center;" > Username or password does not exist! <br><a href="/login.html">Click this link to get redirected to the login page </a></h1> '
    return render_template("login.html", Loginform=Loginform, active_user='user' in session)

@app.route('/logout.html')
@login_required
def logout():
    logout_user()
    session.pop('user', None)
    session.pop('id', None)
    return redirect(url_for('index'))
