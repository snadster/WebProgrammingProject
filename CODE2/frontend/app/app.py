##
##  frontend renders templates and calls logic and db
##
from datetime import date, datetime, timedelta

from flask import make_response, redirect, render_template, request, url_for, Flask
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import select

from app import app
from database.pythonFiles.database import db
from logic.app import app

from database.pythonFiles.user import User
from database.pythonFiles.project import Project
from database.pythonFiles.project import Palette
from database.pythonFiles.project import Counter

import requests
import os


# Start flask
app = Flask(__name__)
app.secret_key = "secret"

#for bugfixing yip
# with app.app_context():
#     db.drop_all()
#     db.create_all()

# logic and db
LOGIC = os.getenv('/logic/app/app.py')
DATA = os.getenv('/database')


###############
#   routes    #
#################################################################
#   everything from views got moved into the app file           #
#   when decomposing to microservices, so there                 #
#   was a more consistent look across the services.             #
#   not my personal favorite setup, but in this context nicer   #
#################################################################

# front page 
@app.route("/")
def frontpage():
    return render_template("frontPage.html")



#################
#   profile     #
###################################################################
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = requests.get(f"{DATA}/pythonFiles/user.py") # currently just all users i assume
        response = user.login(username, password)
        thing = response.json() if response.ok else [] #idk what this does
        return redirect( url_for("profile") )
        # if user and user.password == password:
        #     login_user(user)
        #     return redirect( url_for("profile") )
    # if user doesn't exist
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
@login_required
def profile():
    return render_template("profile.html", 
                           Username = current_user.username,
                           mail = current_user.mail,
                           projects = db.session.scalars(select(Project).where(Project.user == current_user)).all())


################
#   project    #
###################################################################
# project itself (it has a theme cookie)
@app.route("/project/<int:projectID>", methods=["GET", "POST"])
@login_required
def project(projectID: int):
    project = db.session.get(Project, projectID)
    if project.user != current_user:
        return redirect(url_for('profile'))

    projects = db.session.scalars(select(Project).where(Project.user == current_user)).all()
    palettes = db.session.scalars(select(Palette)).all()
    counter = db.session.scalars(select(Counter)).all()
    theme = request.cookies.get("theme", "fall")
    if theme == "light":
        return render_template("projectPage.html", 
                                navBarTheme = "/static/CSS/mainPageLight.css",
                                mainTheme = "/static/CSS/navBarLight.css",
                                theme = "Pastel Theme",
                                projectTitle = project.title,
                                projectID = project.id,
                                palette = palettes,
                                date = project.date,
                                counters = project.counters,
                                # notes = project.notes,
                                hookSize = project.hookSize,
                                yarn = project.yarn,
                                pattern = project.pattern,
                                Counter = counter,
                                projects = projects,
                                project = project)
    else:
        return render_template("projectPage.html",
                                navBarTheme = "/static/CSS/navBarFall.css",
                                mainTheme = "/static/CSS/mainPageFall.css",
                                theme = "Fall Theme",
                                projectTitle = project.title,
                                projectID = project.id,
                                palette = palettes,
                                date = project.date,
                                counters = project.counters,
                                # notes = project.notes,
                                hookSize = project.hookSize,
                                yarn = project.yarn,
                                pattern = project.pattern,
                                Counter = counter,
                                projects = projects,
                                project = project)
    
# change from switch to selected theme if want more than two themes (for mvp we don't)
@app.route("/clicked/<int:projectID>")
@login_required
def theme2(projectID: int):
    theme = request.cookies.get("theme", "fall")
    response = make_response(redirect(url_for('project', projectID = projectID)))
    if theme == "light":
        response.set_cookie('theme', "fall",
                            expires=datetime.now() + timedelta(days=30))
    else:
        response.set_cookie('theme', "light",
                            expires=datetime.now() + timedelta(days=30))
    return response


# makes a project in the db with default values
@app.route('/newProject')
@login_required
def newProject():
    user = current_user._get_current_object()
    date_ = date.today()
    title = "My New Project!"
    archived = False
    counters = []
    # notes = []
    hookSize = None
    yarn = None
    pattern = None
    palette = db.session.scalars(select(Palette)).all()
    print(user, type(user))
    project = Project(user, date_, title, archived, 
                      counters, hookSize, yarn, pattern, 
                      palette)
    project.save()
    projectID = project.id
    return redirect(url_for('makeProject',  projectID=projectID))


# gives the user a clean template for a project
@app.route('/makeProject/<int:projectID>')
@login_required
def makeProject(projectID: int):
    project = db.session.get(Project, projectID)
    projects = db.session.scalars(select(Project).where(Project.user == current_user)).all()
    return render_template("projectPage.html",
                    navBarTheme = "/static/CSS/mainPageFall.css",
                    mainTheme = "/static/CSS/navBarFall.css",
                    theme = "Fall Theme",
                    projectTitle = project.title,
                    palettes = db.session.scalars(select(Palette)).all(),
                    # notes = "",
                    hookSize = "none added",
                    yarn = "none added",
                    pattern = "none added",
                    counters = project.counters,
                    projects = projects,
                    project = project)


# save the project to database with user input
@app.route('/saveProject/<int:projectID>', methods=['POST', 'GET'])
@login_required
def saveProject(projectID: int):
    project = db.session.get(Project, projectID)
    project.user = current_user._get_current_object()
    project.date_ = date.today()
    project.title = request.form["title"]
    project.archived = False
    project.counters = []
    # project.notes = request.form.get("notes", default=[])
    project.hookSize = request.form.get("needle", default="")
    project.yarn = request.form.get("yarn", default="")
    project.pattern = request.form.get("pattern", default="")
    project.palette = request.form.get("paletteOp", default=[])
    project.save()
    return redirect(url_for('project', projectID=projectID))

# render archive
@app.route('/archive', methods=['POST', 'GET'])
@login_required
def archive():
    return render_template("archive.html", 
                           projects = db.session.scalars(select(Project).where(Project.user == current_user)).all() )

# archive a project
@app.route('/archiveProject/<int:projectID>', methods=['POST', 'GET'])
@login_required
def archiveProject(projectID: int):
    project = db.session.get(Project, projectID)
    project.user = current_user._get_current_object()
    project.date_ = date.today()  # VALUE WE CHANGE
    project.title = project.title
    project.archived = True # VALUE WE CHANGE
    project.counters = project.counters
    # project.notes = request.form.get("notes", default=[])
    project.hookSize = project.hookSize
    project.yarn = project.yarn
    project.pattern = project.pattern
    project.palette = project.palette
    project.save()
    return redirect(url_for('archive'))

# @app.route('/saveNotes/<int:projectID>', methods=['POST', 'GET'])
# @login_required
# def saveNotes(projectID: int):
#     project = db.session.get(Project, projectID)
#     project.notes.append = request.form.get("notes")
#     project.save()
#     return redirect(url_for('project', projectID=projectID))

#################
#   counters    #
###################################################################
# make new counter
@app.route('/newCounter/<int:projectID>', methods=['POST', 'GET'])
@login_required
def newCounter(projectID: int):
    project = db.session.get(Project, projectID)
    value = 0
    counter = Counter(value, None, None, projectID)
    counter.save()
    project.counters.append(counter)
    return redirect(url_for('project',  projectID=projectID))

# add to counter and minus from counter. 
@app.route('/upCounter/<int:projectID>/<int:counterID>', methods=['POST', 'GET'])
@login_required
def upCounter(counterID: int, projectID: int):
    counter = db.session.get(Counter, counterID)
    counter.id = counterID
    counter.value = counter.value+1
    counter.link = None
    counter.loop = None
    counter.save()
    return redirect(url_for('project',  projectID=projectID))

@app.route('/downCounter/<int:projectID>/<int:counterID>', methods=['POST', 'GET'])
@login_required
def downCounter(counterID: int, projectID: int):
    counter = db.session.get(Counter, counterID)
    counter.id = counterID
    counter.value = counter.value-1
    counter.link = None
    counter.loop = None
    counter.save()
    return redirect(url_for('project',  projectID=projectID))


#######################
#   color palettes    #
###################################################################
# render palettes page
@app.route("/palettes")
@login_required
def palettes():
    palettes = db.session.scalars(select(Palette)).all()
    return render_template("colorPalettes.html",
                           palettes = palettes)
# render make palette page
@app.route("/newPalette")
@login_required
def newPalette():
    return render_template("makePalette.html")

# save the palette to db
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

# delete palette ( non-functional )
@app.route("/deletePalette", methods = ["POST", "GET"])
@login_required
def deletePalette():
    # TODO this doesn't work but it also doesn't say why, eh.
    paletteName = request.form.get('delPal')
    palettes = db.session.scalars(select(Palette)).all()
    for pal in palettes:
        if pal.name == paletteName:
            pal.deletePalette()
    return redirect(url_for('palettes'))
        

#########################
#   REMOVED FROM MVP    #
#######################################################################
# # dev notes
# @app.route("/devNotes")
# def devNotes():
#     return render_template("DevNotes.html")