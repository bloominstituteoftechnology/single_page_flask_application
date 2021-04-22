"""Example of a one file flask application that uses requests to access an API"""
from os import getenv
from datetime import datetime as dt
import requests
from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

DB = SQLAlchemy(app)


# some routes
@app.route("/")
def root():
    astro_data = Astros.query.all()[0]
    return "There are {} people in space as of {}!".format(astro_data.num_astros, astro_data.time_stamp)


@app.route("/update")
def update():
    request = requests.get("http://api.open-notify.org/astros.json")
    astro_data = request.json()
    num_astros = astro_data["number"]
    record = Astros(num_astros=num_astros, time_stamp=dt.utcnow())
    DB.session.add(record)
    DB.session.commit()

    return redirect("/")


@app.route("/reset")
def reset():
    DB.drop_all()
    DB.create_all()
    return redirect("/")


class Astros(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    num_astros = DB.Column(DB.Integer, nullable=False)
    time_stamp = DB.Column(DB.String, nullable=False)

    def __repr__(self):
        return "There are %s astros!" % self.num_astros
