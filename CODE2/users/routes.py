
########################
#   LOGIN AND PROFILE  #
#########################################################
from flask import app, jsonify, redirect, render_template, request, url_for
from flask_login import login_user

from user import User

#TODO
# this for sure does not work or is even close to correct
# but on the other hand he literally never taught us this
@app.route("/login", methods=["GET", "POST"])
def login(data):
    if request.method == "POST":
        uname = data.username
        pword = data.password
        user = User.get_by_username(uname)
        if user and user.password == pword:
            login_user(user)
            return True
        return False

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    email = request.form["mail"]
    user = User(username, password, email)
    user.save()
    return redirect(url_for("frontpage"))

