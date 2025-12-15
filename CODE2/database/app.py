
##
##  database is our project database and etc
##

import os
from flask import Flask

from database.pythonFiles import login
from database.pythonFiles import database
from logic.app import app

# logic
LOGIC = os.getenv('/logic')

# Database stuff
database.init_db(app, "sqlite:///database.db")
database.setup_db(app)
