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
# import project
# import counter


# for bug fixing
with app.app_context():
    db.drop_all()
    db.create_all()

# Import the views
# import app.py # for some reaon can't be resolved
