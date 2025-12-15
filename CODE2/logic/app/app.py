##
##  logic should have login abilities
##
from database.pythonFiles import login
from frontend.app import app
from flask import Flask, jsonify, request

# Login Manager
login.init_login_manager(app)


#################
#   functions   #
#################################################################

def login(username: str, password: str):
    pass

## i assume we somehow login here but also flask can handle logins
## so really what i think i want here is a call to the db
## and then a response of whether or not a user was logged in.
##