# Setup inspired by
# https://flask.palletsprojects.com/en/stable/patterns/packages/

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

# Start flask
app = Flask(__name__)
app.secret_key = "secret"

# Database stuff
class Base(DeclarativeBase, MappedAsDataclass):
    pass

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db = SQLAlchemy(app, model_class=Base)

# Setup the database
import pythonFiles.counter
import pythonFiles.palette
import pythonFiles.project
import pythonFiles.project_to_palette
import pythonFiles.user

# for bug fixing
with app.app_context():
    db.drop_all()
    db.create_all()

# Import the views, except its mad at me when i do so
# import app.py 
