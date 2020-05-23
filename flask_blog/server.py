import sys, os
from flask import Flask
app = Flask(__name__)

# URL Routing - Home Page
@app.route("/")
def index():
    return "Hello World!"

# Main Function, Runs at http://0.0.0.0:8000
if __name__ == "__main__":
    app.run(port=8000)

@app.route("/welcome/")
def welcome():
    return "Welcome to my webpage!"
