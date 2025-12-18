
from flask import Flask, session

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

import database
from database import db
import login

# Start flask
app = Flask(__name__)
app.secret_key = "secret"

# Database stuff
database.init_db(app, "sqlite:///database.db")
database.setup_db(app)


#############
#   ROUTES  #
#########################################################

from flask import jsonify, redirect, render_template, request, url_for

from user import User

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.form
        uname = data["username"]
        pword = data["password"]
        user = User.get_by_username(uname)
        if user and user.password == pword:
            session["current_user"] = user.id 
            return {"ok": True}
        return {"ok": False}

@app.route("/register", methods=["POST"])
def register():
    data = request.form
    user = User(data["username"], data["password"], data["email"])
    user.save()
    return {"ok": True}

@app.route("/getUserID", methods=["GET"])
def getUser():
    data = request.form
    user = User.get_by_username(data["username"])
    return {"user_id": user.id}