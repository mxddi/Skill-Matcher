from flask import Flask, render_template

app = Flask("__name__")

from . import db
db.init_app(app)

@app.route("/")
def index():
    return render_template("index.html")