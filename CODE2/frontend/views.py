from datetime import date, datetime, timedelta

from flask import make_response, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import select

import app
import projects
import requests

# front page 
@app.route("/")
def frontpage():
    return render_template("frontPage.html")

# profile
@app.route("/profile", methods=["POST", "GET"])
@login_required
def profile():
    # TODO i assume the get doesn't actually work.
    response = requests.get("HTTP://projects:5000/database")
    projects = response.json() if response.ok else[]
    return render_template("profile.html", 
                           Username = current_user.username,
                           mail = current_user.mail,
                           projects = projects)

##########################
##      PALETTES        ##
##############################################################

@app.route("/palettes")
@login_required
def palettes():
    response = requests.get("HTTP://palettes:5000/database")
    palettes = response.json() if response.ok else[]
    return render_template("colorPalettes.html",
                           palettes = palettes)

@app.route("/newPalette")
@login_required
def newPalette():
    return render_template("makePalette.html")

##########################
##      PROJECTS        ##
#############################################################
@app.route("/project/<int:projectID>", methods=["GET", "POST"])
@login_required
def project(projectID: int):
    # boot people if it's not their project
    response = requests.get((f"HTTP://projects:5000/database/{projectID}"))
    project = response.json() if response.ok else[]
    if project.user != current_user:
        return redirect(url_for('profile'))
    
    # we need to request a cookie from the projects backend. idk how.
    response1 = requests.get("HTTP://projects:5000/database")
    projects = response1.json() if response1.ok else[]

    response2 = requests.get("HTTP://palettes:5000/database")
    palettes = response2.json() if response2.ok else[]

    response3 = requests.get("HTTP://projects:5000/database/counter")
    counter = response3.json() if response3.ok else[]

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
                                Counter = counter, #i don't think we need this one
                                projects = projects, #all projects to display in sidebar
                                project = project) # project found via id
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

# gives the user a clean template for a project
@app.route('/makeProject/<int:projectID>')
@login_required
def makeProject(projectID: int):
    response = requests.get("HTTP://projects:5000/database/projectID")
    project = response.json() if response.ok else[]

    response1 = requests.get("HTTP://projects:5000/database")
    projects = response1.json() if response1.ok else[]

    response2 = requests.get("HTTP://palettes:5000/database")
    palettes = response2.json() if response2.ok else[]
    return render_template("projectPage.html",
                    navBarTheme = "/static/CSS/mainPageFall.css",
                    mainTheme = "/static/CSS/navBarFall.css",
                    theme = "Fall Theme",
                    projectTitle = project.title,
                    palettes = palettes,
                    hookSize = "none added",
                    yarn = "none added",
                    pattern = "none added",
                    counters = project.counters,
                    projects = projects,
                    project = project)

# render archive page
@app.route('/archive', methods=['POST', 'GET'])
@login_required
def archive():
    response1 = requests.get("HTTP://projects:5000/database")
    projects = response1.json() if response1.ok else[]

    return render_template("archive.html", 
                           projects = projects )


##########################
##      USERS           ##
##################################################################

# we need to remove the logic and keep the render template
@app.route("/login", methods=["GET", "POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    payload = {username, password}
    response = requests.post('HTTP://user:5000/login', data = payload)
    user = response.json() if response.ok else[]
    # TODO this probably won't work
    if user:
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('frontpage'))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("frontpage"))


