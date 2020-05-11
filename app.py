from flask import Flask, request, Response, render_template
import requests
import itertools
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import Regexp, ValidationError, Optional
import re
from flask.json import jsonify
from jira import JIRA

csrf = CSRFProtect()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

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
