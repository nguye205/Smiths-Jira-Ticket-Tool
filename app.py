from flask import Flask, session, request, Response, render_template, redirect, url_for
import requests
import itertools
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, BooleanField
from wtforms.validators import Regexp, ValidationError, Optional, InputRequired, Email, Length
import re
from flask.json import jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from random import seed, randint
import sqlite3


csrf = CSRFProtect()
app = Flask(__name__)
app.config["SECRET_KEY"] = "row the boat"
csrf.init_app(app)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_mng = LoginManager(app)
login_mng.login_view = 'login'

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=40)])
    rememberme = BooleanField('Remember me')

class UserAccount(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(40))

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['POST','GET'])
def login():
    Loginform = LoginForm()

    if Loginform.validate_on_submit():
        print("Checking")
        user = UserAccount.query.filter_by(username=Loginform.username.data).first() # only get one result
        if user:        # if user exists, get the Password
            if check_password_hash(user.password, Loginform.password.data):
            # if user.password == form.password.data:
                login_user(user, remember=Loginform.rememberme.data)
                session['id'] = user.id
                session['user'] = user.username
                return redirect(url_for('index'))
        #return '<h1>Username or password does not exist</h1> <a href="/">GO TO HOME </a>'# if user doesn't exist
        return '<h1 style="color: #111;font-size: 25px; font-weight: bold; letter-spacing: -1px; line-height: 1; text-align: center;" > Username or password does not exist! <br><a href="/login.html">Click this link to get redirected to the login page </a></h1> '
    print("Not valid")
    return render_template("login.html", Loginform=Loginform, active_user='user' in session)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('user', None)
    session.pop('id', None)
    return redirect(url_for('index'))
