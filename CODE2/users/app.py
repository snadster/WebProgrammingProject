
from flask import Flask

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

# Login Manager
login.init_login_manager(app)


#############
#   ROUTES  #
#########################################################

from flask import app, jsonify, redirect, render_template, request, url_for
from flask_login import login_user

from user import User

#TODO
# this for sure does not work or is even close to correct
# but on the other hand he literally never taught us this
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.data
        uname = data.username
        pword = data.password
        user = User.get_by_username(uname)
        if user and user.password == pword:
            login_user(user)
            return user
        return []

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    email = request.form["mail"]
    user = User(username, password, email)
    user.save()
    return redirect(url_for("frontpage"))
