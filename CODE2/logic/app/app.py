##
##  logic should have login abilities
##
from database.pythonFiles import login
from frontend.app import app
from flask import Flask, jsonify, request
import requests
import os
from flask_login import LoginManager

from database.pythonFiles import user

# database, now a circular import, because im a dumbass
DATA = os.getenv('/database')

# Login Manager
login.init_login_manager(app)


#################
#   functions   #
#################################################################

# def login(username: str, password: str):
#     user = requests.get(f"{DATA}/pythonFiles/user.py") # currently just all users i assume
#     pass

## i assume we somehow login here but also flask can handle logins
## so really what i think i want here is a call to the db
## and then a response of whether or not a user was logged in.
##

login_manager = LoginManager()

def init_login_manager(app):
    login_manager.init_app(app)
    login_manager.session_protection = "strong"
    # throw people who aren't logged in to the front page if they try to access something
    login_manager.login_view = "frontpage" 

@login_manager.user_loader
# creative name i know. Checks if user exists in database
def load_user(user_id):
    response = requests.get(f"{DATA}/pythonFiles/user.py")
    users = response.json() if response.ok else [] # response.json() gives me all the data in vague dictionary form, and goes [200]-all good
    # now somehow check whether the userID exists in the users 
    return user.User.get_by_id(user_id)