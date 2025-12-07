from datetime import datetime, timedelta

from flask import make_response, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import select

from main import app
from pythonFiles.database import db

from pythonFiles.user import User
from pythonFiles.project import Project
from pythonFiles.project import Palette

# front page 
@app.route("/")
def frontpage():
    return render_template("frontPage.html")


########################
#   LOGIN AND PROFILE  #
#########################################################
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.get_by_username(username)
        if user and user.password == password:
            login_user(user)
            return redirect( url_for("profile") )

    return render_template("frontPage.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("frontpage"))

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    email = request.form["mail"]
    user = User(username, password, email)
    user.save()
    return redirect(url_for("frontpage"))

# profile
@app.route("/profile", methods=["POST", "GET"])
def profile():
    return render_template("profile.html", 
                           Username = User.username,
                           mail = User.mail)
##########################################################


#################
#   PROJECT     #
#############################################################################
# project itself (it has a theme cookie)
# btw we need to redirect to correct project by checking
# which one they requested (somehow)
# maybe ask for the ID associated with the one they clicked (from db),
# and then pull the information belonging to that one.
@app.route("/project", methods=["GET", "POST"])
# @login_required
def project():
    palettes = db.session.scalars(select(Palette)).all()
    theme = request.cookies.get("theme", "fall")
    if theme == "light":
        return render_template("projectPage.html", 
                                navBarTheme = "/static/CSS/mainPageLight.css",
                                mainTheme = "/static/CSS/navBarLight.css",
                                theme = "Pastel Theme",
                                projectTitle = Project.title,
                                projectID = Project.id,
                                palette = palettes,
                                date = Project.date,
                                counters = Project.counters,
                                notes = Project.notes,
                                hookSize = Project.hookSize,
                                yarn = Project.yarn,
                                pattern = Project.pattern)
    else:
        return render_template("projectPage.html",
                                navBarTheme = "/static/CSS/navBarFall.css",
                                mainTheme = "/static/CSS/mainPageFall.css",
                                theme = "Fall Theme",
                                projectTitle = Project.title,
                                projectID = Project.id,
                                palette = palettes,
                                date = Project.date,
                                counters = Project.counters,
                                notes = Project.notes,
                                hookSize = Project.hookSize,
                                yarn = Project.yarn,
                                pattern = Project.pattern)

# change from switch to selected theme if want more than two themes (for mvp we don't)

@app.route("/clicked")
def theme2():
    theme = request.cookies.get("theme", "fall")
    response = make_response(redirect('/project'))
    if theme == "light":
        response.set_cookie('theme', "fall",
                            expires=datetime.now() + timedelta(days=30))
    else:
        response.set_cookie('theme', "light",
                            expires=datetime.now() + timedelta(days=30))
    return response


# project
@app.route('/newProject')
# @login_required
def newProject():
    return redirect(url_for('project'))

# somehow make sure it redirects to the correct project using its ID
@app.route('/saveProject', methods=['POST'])
#@login_required
def saveProject():
    user = current_user
    date = datetime.today().strftime('%Y-%m-%d')
    title = request.form["title"]
    archived = False
    counters = 0
    notes = request.form["notes"]
    hookSize = None 
    yarn = request.form["yarn"]
    pattern = request.form["pattern"]
    project = Project(user, date, title, archived, 
                      counters, notes, hookSize, yarn, pattern)
    project.save()
    return redirect(url_for('project'), )


# @app.route('/archiveProject', methods=['POST', 'GET'])
# @login_required
# def archiveProject():

##################################################################

#####################
# COLOR PALETTES    #
##################################################################
@app.route("/palettes")
@login_required
def palettes():
    palettes = db.session.scalars(select(Palette)).all()
    return render_template("colorPalettes.html",
                           palettes = palettes)

@app.route("/newPalette")
@login_required
def newPalette():
    return render_template("makePalette.html")

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



#########################
#   REMOVED FROM MVP    #
#######################################################################
# # dev notes
# @app.route("/devNotes")
# def devNotes():
#     return render_template("DevNotes.html")