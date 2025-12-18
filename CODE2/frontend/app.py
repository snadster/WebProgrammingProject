
from flask import Flask, session

# Start flask
app = Flask(__name__)
app.secret_key = "secret"

#for bugfixing yip
# with app.app_context():
#     db.drop_all()
#     db.create_all()

#################
#   routes  #
########################################
from datetime import date, datetime, timedelta

from flask import make_response, redirect, render_template, request, url_for
from sqlalchemy import select

import requests

# front page 
@app.route("/")
def frontpage():
    return render_template("frontPage.html")

# profile
@app.route("/profile", methods=["POST", "GET"])
def profile():
    if( userLoggedIn() ):
        response = requests.get("HTTP://projects:5000/database")
        projects = response.json() if response.ok else[]
        return render_template("profile.html", 
                            Username = current_user.username,
                            mail = current_user.mail,
                            projects = projects)
    else:
        return redirect(url_for('frontpage'))

##########################
##      PALETTES        ##
##############################################################

@app.route("/palettes")
def palettes():
    if( userLoggedIn() ):
        response = requests.get("HTTP://palettes:5000/database")
        palettes = response.json() if response.ok else[]
        return render_template("colorPalettes.html",
                            palettes = palettes)
    else:
        return redirect(url_for('frontpage'))

@app.route("/newPalette")
def newPalette():
    if( userLoggedIn() ):
        return render_template("makePalette.html")
    else:
        return redirect(url_for('frontpage'))

@app.route("/savePalette")
def savePalette():
    if( userLoggedIn() ):
        title = request.form["pTitle"]
        color1 = request.form["color1"]
        color2 = request.form["color2"]
        color3 = request.form["color3"]
        color4 = request.form["color4"]
        color5 = request.form["color5"]
        color6 = request.form["color6"]
        color7 = request.form["color7"]
        color8 = request.form["color8"]
        palette = {"title": title,"color1":color1, "color2":color2, "color3":color3, "color4":color4, "color5":color5, "color6":color6, "color7":color7, "color8":color8}
        requests.get("HTTP://palettes:5000/savePalette", data = palette)
        return redirect(url_for('newPalette'))
    else:
        return redirect(url_for('frontpage'))

##########################
##      PROJECTS        ##
#############################################################
@app.route("/project/<int:projectID>", methods=["GET", "POST"])
def project(projectID: int):
    if( userLoggedIn() ):
        # boot people if it's not their project
        response = requests.get((f"HTTP://projects:5000/database/{projectID}"))
        project = response.json() if response.ok else[]

        response = requests.get(("HTTP://projects:5000/getUser"))
        u = response.json() if response.ok else[]

        if u.user != current_user:
            return redirect(url_for('profile'))
        
        # we need to request a cookie from the projects backend. idk how.
        response1 = requests.get("HTTP://projects:5000/database")
        projects = response1.json() if response1.ok else[]

        response2 = requests.get(f"HTTP://palettes:5000/getPalette", data = {"projectID":projectID})
        palette = response2.json() if response2.ok else[]

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
                                    palette = palette,
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
    else:
        return redirect(url_for('frontpage'))

@app.route('/newProject')
def newProject():
    if( userLoggedIn() ):
        response = requests.get(f"HTTP://projects:5000/newProject")
        project = response.json() if response.ok else[]
        return redirect(url_for('makeProject',  projectID= project.id ))
    else:
        return redirect(url_for('frontpage'))


# gives the user a clean template for a project
@app.route('/makeProject/<int:projectID>')
def makeProject(projectID: int):
    if( userLoggedIn() ):
        response = requests.get(f"HTTP://projects:5000/database/{projectID}")
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
    else:
        return redirect(url_for('frontpage'))


@app.route('/saveProject/<int:projectID>')
def saveProject(projectID: int):
    if( userLoggedIn() ):
        title = request.form["title"]
        hookSize = request.form.get("needle", default="")
        yarn = request.form.get("yarn", default="")
        pattern = request.form.get("pattern", default="")
        palette = request.form.get("paletteOp", default=[])
        payload = {"projectID":projectID, "title":title, "hookSize":hookSize, "yarn":yarn, 
                "pattern": pattern, "palette":palette}

        response = requests.post('HTTP://users:5000/saveProject', data = payload)
        project = response.json() if response.ok else[]
        return redirect(url_for('project', projectID=project.id))
    else:
        return redirect(url_for('frontpage'))

@app.route('/archiveProject/<int:projectID>')
def archiveProject(projectID: int):
    if( userLoggedIn() ):
        requests.get("HTTP://projects:5000/archiveProject", data = {"projectID":projectID})
        return redirect(url_for('archive'))
    else:
        return redirect(url_for('frontpage'))

# render archive page
@app.route('/archive', methods=['POST', 'GET'])
def archive():
    if( userLoggedIn() ):
        response1 = requests.get("HTTP://projects:5000/database")
        projects = response1.json() if response1.ok else[]

        return render_template("archive.html", 
                            projects = projects )
    else:
        return redirect(url_for('frontpage'))


##########################
##      USERS           ##
##################################################################
def userLoggedIn():
    return "userID" in session.keys()

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    email = request.form["mail"]
    user = {"username": username, "password": password, "email":email}
    requests.post('HTTP://users:5000/register', data = user)
    return redirect(url_for("frontpage"))


# we need to remove the logic and keep the render template
@app.route("/login", methods=["GET", "POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    data = {"username": username}
    response = requests.get('HTTP://users:5000/getUserID', data = data)
    userID = response.json()["user_id"] if response.ok else []
    payload = {"username":username, "password":password}
    response = requests.post('HTTP://users:5000/login', data = payload)
    user = response.json() if response.ok else[]
    if user:
        session["userID"] = userID
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('frontpage'))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("frontpage"))
