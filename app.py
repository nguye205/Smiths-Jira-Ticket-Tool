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
    description = TextAreaField('Description', validators=[InputRequired()])
    pumpSerialNumber = StringField('Pump Serial Number', validators=[InputRequired()])
    library = StringField('Library', validators=[InputRequired()])
    firmwareVersion = StringField('Firmware Version', validators=[InputRequired()])
    others = TextAreaField('Others')
    project = SelectField('Project', choices=[('','-'),('SMPUMP','SMPUMP'),('SAN','SAN')], validators=[InputRequired()])

def getFormValues():
    #API VARIABLES these only need to be updated once
    user = 'colin.ducklow@smiths-medical.com' #update string to your own email address
    apikey = '<APIKEY>' #update string to your JIRA API key. ex.) egkKeNabcdefglgLuDi95A7

    #DYNAMIC VARIABLES Update the variables below for each bug ticket. Optionally you can edit these variables on the JIRA ticket after the ticket has been created
    SSTP = "<SSTP ID>" #replace this with the SSTP # Ex)SSTP2400-0103 where the bug was discovered ( If bug was discovered outside of an SSTP put NA)
    Summary = "<Issue Title here>" #replace string with issue title
    Expected = "<Expected result here>" #replace string with whatever action was expected from the pump
    Actual = "<Actual result here>" #Replace string with the actual action that happened instead of the expected one
    Label = "FormalSVT9" #FormalSVT<number> number = pass number.  If the bug is not part of a formal pass, the label can be an empty string ""
    Pump = "<pump type and serial number>" #ex) LVP 03-90150 and Syringe 02-90100
    Firmware = "<firmware>" #Update this to whatever the most recent firmware(s) used to test the bug, ex) 1.0.0.358
    Library = "CRI-81352-SSTLIB0002-0111 v0.425" #Select your library by UNCOMMENTING/COMMENTING this line
    #Library = "CRI-81352-SSTLIB0001-0110 v0.190" #Select your library by UNCOMMENTING/COMMENTING this line
    SRS = "<Unknown>" #This can be updated with the SRS number if you have it, other wise leave as unknown

    #No need to update the rest of these variables
    server = 'https://smithsforge.atlassian.net'
    StepsToReproduce = "*Steps to reproduce:* \n" + "<Steps to reproduce>\n\n"
    IssueDescription = "*Issue:* " + Summary
    Requirement = "*Requirement:* " + SRS
    TestProcedure = "*Test Procedure:* CRI-81352-"+ SSTP
    Expected = '*Expected Result:* ' + Expected
    Actual = '*Actual Result:* ' + Actual

def submitBugTicket():
    #SUBMIT BUG TICKET
    options = {
     'server': server
    }
    jira = JIRA(options, basic_auth=(user,apikey) )

    jira.create_issue(fields={
        'project': {'key': 'SMPUM'},  #Change SMPUM to SAN for debug/test mode
        'issuetype': {
            "name": "Bug"
        },
        'summary': Summary + " ( CRI-81352-" + SSTP + " " +Label+" )",
        'description': TestProcedure +"\n" +Requirement +"\n\n"+ IssueDescription +"\n\n"+ StepsToReproduce + Expected +"\n\n"+ Actual,
        'labels': [Label],
        'environment': "*Pump:* "+Pump+"\n*Firmware:* "+Firmware+ "\n*Library:* "+Library,

    })

@app.route('/', methods=['POST','GET'])
def index():
    ticketForm = TicketForm()
    if ticketForm.is_submitted():
        print (".............submitted")
    if ticketForm.validate():
        print ("valid")
    if ticketForm.validate_on_submit():
        return '<h1>valid</h1>'
    return render_template("index.html", ticketForm=ticketForm)
