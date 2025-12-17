from flask import jsonify
from flask_login import current_user
from sqlalchemy import select
from palette import Palette
import app
from database import db

#####################
# COLOR PALETTES    #
##################################################################
@app.route("/database", methods = ["GET"])
def getPalettes():
    palettes = db.session.scalars(select(Palette).where(Palette.user == current_user)).all()
    return jsonify([{
                "id": pl.id, "name": pl.name,
                "color1": pl.color1, "color2": pl.color2,
                "color3": pl.color3, "color4": pl.color4,
                "color5": pl.color5, "color6": pl.color6,
                "color7": pl.color7, "color8": pl.color8}
                for pl in palettes])

@app.route("/savePalette", methods = ["POST"])
@login_required
def savePalette():
    title = request.form["pTitle"]
    color1 = request.form["color1"]
    color2 = request.form["color2"]
    color3 = request.form["color3"]
    color4 = request.form["color4"]
    color5 = request.form["color5"]
    color6 = request.form["color6"]
    color7 = request.form["color7"]
    color8 = request.form["color8"]
    palette = Palette(title,color1, color2, color3, color4, color5, color6, color7, color8)
    palette.save()
    return redirect(url_for('newPalette'))


