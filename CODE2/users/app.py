from flask import Flask, request

import database
from user import User

# Start flask
app = Flask(__name__)
app.secret_key = "secret"

# Database stuff
database.init_db(app, "sqlite:///database.db")
database.setup_db(app)

#########################################################
#                     ROUTES                            #
#########################################################


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    uname = data["username"]
    pword = data["password"]
    user = User.get_by_username(uname)
    if user and user.password == pword:
        return {"ok": True, "id": user.id, "username": user.username}
    return {"ok": False}, 404


@app.route("/register", methods=["POST"])
def register():
    data = request.json
    user = User(data["username"], data["password"], data["email"])
    user.save()
    return {"ok": True}


@app.route("/getUser", methods=["GET"])
def getUser():
    data = request.json
    user = User.get_by_id(data["id"])
    return {"id": user.id, "username": user.username, "mail": user.mail}
