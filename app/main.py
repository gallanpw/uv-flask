from flask import Flask

app = Flask(__name__)


@app.route("/")
def welcome():
    return {"message": "Welcome!"}


@app.route("/hello")
def hello_world():
    return {"message": "Hello World!"}
