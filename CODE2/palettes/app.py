from flask import Flask, request, jsonify
from sqlalchemy import select

import database
from database import db
from palette import Palette


# Start flask
app = Flask(__name__)
app.secret_key = "secret"

# Database stuff
database.init_db(app, "sqlite:///database.db")
database.setup_db(app)


#############
#   ROUTES  #
##################################################################

#####################
# COLOR PALETTES    #
##################################################################

@app.route("/palettes/<int:userID>", methods=["GET"])
def database(userID: int):
    palettes = db.session.scalars(select(Palette).where(Palette.userID == userID)).all()
    return jsonify([palette.toDict() for palette in palettes])


@app.route('/palettes/<int:userID>/<int:paletteID>', methods=['GET'])
def getPalette(userID: int, paletteID: int):
    palette = db.session.get(Palette, paletteID)
    if palette.userID == userID:
        return jsonify(palette.toDict())
    else:
        return {}, 404


@app.route("/savePalette", methods = ["POST"])
def savePalette():
    palette = request.json
    title = palette["title"]
    userID = palette["userID"]
    color1 = palette["color1"]
    color2 = palette["color2"]
    color3 = palette["color3"]
    color4 = palette["color4"]
    color5 = palette["color5"]
    color6 = palette["color6"]
    color7 = palette["color7"]
    color8 = palette["color8"]
    newPalette = Palette(userID, title, color1, color2, color3, color4, color5, color6, color7, color8)
    newPalette.save()
    return {"ok": True}
