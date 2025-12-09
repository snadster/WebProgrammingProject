from datetime import date, datetime, timedelta

from flask import make_response, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import select

from main import app
from pythonFiles.database import db

from pythonFiles.user import User
from pythonFiles.project import Project
from pythonFiles.project import Palette
from pythonFiles.project import Counter

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
@login_required
def profile():
    return render_template("profile.html", 
                           Username = current_user.username,
                           mail = current_user.mail)
##########################################################


#################
#   PROJECT     #
#############################################################################
# project itself (it has a theme cookie) fuck fix give it project as object goddamnit
@app.route("/project/<int:projectID>", methods=["GET", "POST"])
@login_required
def project(projectID: int):
    project = db.session.get(Project, projectID)
    projects = db.session.scalars(select(Project)).all()
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
                                notes = project.notes,
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
                                notes = project.notes,
                                hookSize = project.hookSize,
                                yarn = project.yarn,
                                pattern = project.pattern,
                                Counter = counter,
                                projects = projects,
                                project = project)

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


# makes a project in the db with default values (html bugs otherwise)
@app.route('/newProject')
@login_required
def newProject():
    user = current_user._get_current_object()
    #date = datetime.today().strftime('%Y-%m-%d')
    date_ = date.today()
    title = "My New Project!"
    archived = False
    counters = []
    notes = ""
    hookSize = None
    yarn = None
    pattern = None
    palette = db.session.scalars(select(Palette)).all()
    print(user, type(user))
    project = Project(user, date_, title, archived, 
                      counters, notes, hookSize, yarn, pattern, 
                      palette)
    project.save()
    # my version of trying to get the project id
    projectID = project.id
    return redirect(url_for('makeProject',  projectID=projectID))


# gives the user a clean template for a project
@app.route('/makeProject/<int:projectID>')
@login_required
def makeProject(projectID: int):
    project = db.session.get(Project, projectID)
    projects = db.session.scalars(select(Project)).all()
    return render_template("projectPage.html",
                    navBarTheme = "/static/CSS/mainPageFall.css",
                    mainTheme = "/static/CSS/navBarFall.css",
                    theme = "Fall Theme",
                    projectTitle = project.title,
                    palettes = db.session.scalars(select(Palette)).all(),
                    counters = 0,
                    hookSize = "none added",
                    yarn = "none added",
                    pattern = "none added",
                    Counter = db.session.scalars(select(Counter)).all(),
                    projects = projects,
                    project = project)


# save the project to database with user input
# make the ID the one it gets from makeProject
@app.route('/saveProject/<int:projectID>', methods=['POST'])
@login_required
def saveProject(projectID: int):
    project = db.session.get(Project, projectID)
    project.user = current_user._get_current_object()
    project.date_ = date.today()
    project.title = request.form["title"]
    project.archived = False
    project.counters = []
    project.hookSize = request.form.get("needle", default="")
    project.yarn = request.form.get("yarn", default="")
    project.pattern = request.form.get("pattern", default="")
    project.palette = request.form.get("paletteOp", default=[])
    project.save()
    return redirect(url_for('project', projectID=projectID))

# @app.route('/saveNotes/<int: projectID>', methods=['POST', 'GET'])
# def saveNotes():
#     date = datetime.today().strftime('%Y-%m-%d')
#     pass


# @app.route('/archiveProject', methods=['POST', 'GET'])
# @login_required
# def archiveProject():

##################################################################

#################
#   COUNTERS    #
##################################################################

@app.route('/newCounter', methods=['POST', 'GET'])
@login_required
def newCounter(projectID):
    project = db.session.get(Project, projectID)
    value = 0
    counter = Counter(value, None, None, projectID)
    counter.save()
    project.counters.append(counter)
    return redirect(url_for('project',  projectID=projectID))

# add to counter and minus from counter. 
# Yes they're basically the same code, no I couldn't 
# as of this moment bother putting them into one function
@app.route('/upCounter', methods=['POST', 'GET'])
@login_required
def upCounter(counterID, projectID):
    counter = db.session.get(Counter, counterID)
    counter.value = counter.value+1
    return redirect(url_for('project',  projectID=projectID))

@app.route('/downCounter', methods=['POST', 'GET'])
@login_required
def downCounter(counterID, projectID):
    counter = db.session.get(Counter, counterID)
    counter.value = counter.value-1
    return redirect(url_for('project', projectID))

# @app.route('/linkCounter', methods=['POST', 'GET'])
# def linkCounter(counterID, projectID):

#     return redirect(url_for('project'), projectID)

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

@app.route("/deletePalette", methods = ["POST", "GET"])
@login_required
def deletePalette():
    # TODO this is probably a bug. I am tired tho.
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