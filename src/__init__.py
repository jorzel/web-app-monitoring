from flask import Flask

app = Flask(__name__)


@app.route("/")
def up():
    return "I am running!"
