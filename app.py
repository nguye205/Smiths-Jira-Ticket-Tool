from flask import Flask, request, Response, render_template
import requests
import itertools
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField
from wtforms.validators import Regexp, Optional, InputRequired, Email, Length
import re
from flask.json import jsonify
from jira import JIRA
from flask_bootstrap import Bootstrap

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
    pumpSerialNumber = StringField('Pump Serial Number', validators=[InputRequired()])
    library = StringField('Library', validators=[InputRequired()])
    firmwareVersion = StringField('Firmware Version', validators=[InputRequired()])
    others = TextAreaField('Others')
    project = SelectField('Project', choices=[('','-'), ('SAN','SAN')], validators=[InputRequired()])

def submitBugTicket(ticketForm):
    user = 'colin.ducklow@smiths-medical.com' #update string to your own email address
    apikey = '<APIKEY>' #update string to your JIRA API key. ex.) egkKeNabcdefglgLuDi95A7

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
    IssueDescription = "*Issue:* " + Summary
    Requirement = "*Requirement:* " + SRS
    TestProcedure = "*Test Procedure:* CRI-81352-"+ SSTP
    Expected = '*Expected Result:* ' + Expected
    Actual = '*Actual Result:* ' + Actual

    options = {
     'server': server
    }

    print (Project)
    print (Summary + " ( CRI-81352-" + SSTP + " " +Label+" )")
    print (TestProcedure +"\n" +Requirement +"\n\n"+ IssueDescription +"\n\n"+ StepsToReproduce +"\n\n" + Expected +"\n\n"+ Actual + "\n\n" + Others)
    print (Label)
    print ("*Pump:* "+Pump+"\n*Firmware:* "+Firmware+ "\n*Library:* "+Library)

    jira = JIRA(options, basic_auth=(user,apikey) )

    jira.create_issue(fields={
        'project': {'key': Project},  #Change SMPUM to SAN for debug/test mode
        'issuetype': {
            "name": "Bug"
        },
        'summary': Summary + " ( CRI-81352-" + SSTP + " " +Label+" )",
        'description': TestProcedure +"\n" +Requirement +"\n\n"+ IssueDescription +"\n\n"+ StepsToReproduce +"\n\n" + Expected +"\n\n"+ Actual + "\n\n" + Others,
        'labels': [Label],
        'environment': "*Pump:* "+Pump+"\n*Firmware:* "+Firmware+ "\n*Library:* "+Library,

    })

@app.route('/', methods=['POST','GET'])
def index():
    ticketForm = TicketForm()
    if ticketForm.validate_on_submit():
        submitBugTicket(ticketForm)
        return '<h1>valid</h1>'
    return render_template("index.html", ticketForm=ticketForm)
