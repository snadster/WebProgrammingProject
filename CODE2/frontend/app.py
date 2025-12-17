
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

from pythonFiles import login
from pythonFiles import database
from pythonFiles.database import db

# Start flask
app = Flask(__name__)
app.secret_key = "secret"

# Database stuff
database.init_db(app, "sqlite:///database.db")
database.setup_db(app)

# Import the views, except its mad at me when i do so
import views

#for bugfixing yip
# with app.app_context():
#     db.drop_all()
#     db.create_all()
