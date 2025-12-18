
from flask import Flask, request

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

import database
from database import db

# Start flask
app = Flask(__name__)
app.secret_key = "secret"

# Database stuff
database.init_db(app, "sqlite:///database.db")
database.setup_db(app)


#############
#   ROUTES  #
#################################################################################

from flask import jsonify
from sqlalchemy import select
from palette import Palette
from database import db

#####################
# COLOR PALETTES    #
##################################################################
@app.route("/database", methods = ["GET"])
def database():
    palettes = db.session.scalars(select(Palette).where(Palette.user == current_user)).all()
    return jsonify([{
                "id": pl.id, "name": pl.name,
                "color1": pl.color1, "color2": pl.color2,
                "color3": pl.color3, "color4": pl.color4,
                "color5": pl.color5, "color6": pl.color6,
                "color7": pl.color7, "color8": pl.color8}
                for pl in palettes])

@app.route('/getPalette', methods=['POST', 'GET'])
def getPalette():
    pid = request.form
    palettes = db.session.scalars(select(Palette).where(Palette.user == current_user)).all()
    palette = palettes.where(Palette.id == pid["projectID"])
    return jsonify([{
                "id": pl.id, "name": pl.name,
                "color1": pl.color1, "color2": pl.color2,
                "color3": pl.color3, "color4": pl.color4,
                "color5": pl.color5, "color6": pl.color6,
                "color7": pl.color7, "color8": pl.color8}
                for pl in palette])

@app.route("/savePalette", methods = ["POST"])
def savePalette():
    palette = request.form
    title = palette["title"]
    color1 = palette["color1"]
    color2 = palette["color2"]
    color3 = palette["color3"]
    color4 = palette["color4"]
    color5 = palette["color5"]
    color6 = palette["color6"]
    color7 = palette["color7"]
    color8 = palette["color8"]
    newPalette = Palette(title,color1, color2, color3, color4, color5, color6, color7, color8)
    newPalette.save()
    pid  = newPalette.id
    return {"id": pid}


