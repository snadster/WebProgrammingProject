from datetime import date, datetime, timedelta

from flask import Flask, make_response, session, redirect, render_template, request, url_for
import requests


# Start flask
app = Flask(__name__)
app.secret_key = "secret"


#################
#   routes  #
########################################


# front page 
@app.route("/")
def frontpage():
    return render_template("frontPage.html")


# profile
@app.route("/profile", methods=["POST", "GET"])
def profile():
    if userLoggedIn():
        userID = session["userID"]
        response = requests.get(f"HTTP://projects:5000/projects/{userID}")
        projects = response.json() if response.ok else []
        responseUser = requests.get("HTTP://users:5000/getUser", json={"id": userID})
        user = responseUser.json() if response.ok else {}
        return render_template("profile.html",
                            Username = user.get("username"),
                            mail = user.get("mail"),
                            projects = projects)
    else:
        return redirect(url_for('frontpage'))


##########################
##      PALETTES        ##
##############################################################

@app.route("/palettes")
def palettes():
    if userLoggedIn():
        userID = session["userID"]
        response = requests.get(f"HTTP://projects:5000/projects/{userID}")
        projects = response.json() if response.ok else []
        response = requests.get(f"HTTP://palettes:5000/palettes/{userID}")
        palettes = response.json() if response.ok else []
        return render_template("colorPalettes.html",
                               palettes = palettes,
                               projects = projects)
    else:
        return redirect(url_for('frontpage'))

@app.route("/newPalette")
def newPalette():
    if userLoggedIn():
        return render_template("makePalette.html")
    else:
        return redirect(url_for('frontpage'))

@app.route("/savePalette", methods=["POST"])
def savePalette():
    if userLoggedIn():
        title = request.form["pTitle"]
        userID = session["userID"]
        color1 = request.form["color1"]
        color2 = request.form["color2"]
        color3 = request.form["color3"]
        color4 = request.form["color4"]
        color5 = request.form["color5"]
        color6 = request.form["color6"]
        color7 = request.form["color7"]
        color8 = request.form["color8"]
        palette = {"title": title, "userID": userID, "color1": color1, "color2": color2,
                   "color3": color3, "color4": color4, "color5": color5,
                   "color6": color6, "color7": color7, "color8": color8}
        requests.post("HTTP://palettes:5000/savePalette", json = palette)
        return redirect(url_for('newPalette'))
    else:
        return redirect(url_for('frontpage'))


##########################
##      PROJECTS        ##
#############################################################

@app.route("/clicked/<int:projectID>")
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


@app.route("/project/<int:projectID>", methods=["GET", "POST"])
def project(projectID: int):
    if userLoggedIn():
        userID = session["userID"]
        response = requests.get(f"HTTP://projects:5000/projects/{userID}/{projectID}")
        project = response.json() if response.ok else None

        if project == None:
            return redirect(url_for('profile'))
        
        else:
            response1 = requests.get(f"HTTP://projects:5000/projects/{userID}")
            projects = response1.json() if response1.ok else []

            palette = None
            paletteID = project["paletteID"]
            if paletteID != None:
                response2 = requests.get(f"HTTP://palettes:5000/palettes/{userID}/{paletteID}")
                palette = response2.json() if response2.ok else None

            response3 = requests.get(f"HTTP://projects:5000/projects/{userID}/{projectID}/counters")
            counter = response3.json() if response3.ok else []

            theme = request.cookies.get("theme", "fall")
            if theme == "light":
                return render_template("projectPage.html", 
                                        navBarTheme = "/static/CSS/mainPageLight.css",
                                        mainTheme = "/static/CSS/navBarLight.css",
                                        theme = "Pastel Theme",
                                        projectTitle = project["title"],
                                        projectID = project["id"],
                                        palette = palette,
                                        date = project["date"],
                                        counters = project["counters"],
                                        # notes = project.notes,
                                        hookSize = project["hookSize"],
                                        yarn = project["yarn"],
                                        pattern = project["pattern"],
                                        Counter = counter, #i don't think we need this one
                                        projects = projects, #all projects to display in sidebar
                                        project = project) # project found via id
            else:
                return render_template("projectPage.html",
                                        navBarTheme = "/static/CSS/navBarFall.css",
                                        mainTheme = "/static/CSS/mainPageFall.css",
                                        theme = "Fall Theme",
                                        projectTitle = project["title"],
                                        projectID = project["id"],
                                        palette = palettes,
                                        date = project["date"],
                                        counters = project["counters"],
                                        # notes = project.notes,
                                        hookSize = project["hookSize"],
                                        yarn = project["yarn"],
                                        pattern = project["pattern"],
                                        Counter = counter,
                                        projects = projects,
                                        project = project)
    else:
        return redirect(url_for('frontpage'))

@app.route('/newProject')
def newProject():
    if userLoggedIn():
        user = {"userID": session["userID"]}
        response = requests.post("HTTP://projects:5000/newProject", json = user)
        project = response.json() if response.ok else[]
        return redirect(url_for('makeProject',  projectID = project["id"] ))
    else:
        return redirect(url_for('frontpage'))


# gives the user a clean template for a project
@app.route('/makeProject/<int:projectID>')
def makeProject(projectID: int):
    if userLoggedIn():
        userID = session["userID"]
        response = requests.get(f"HTTP://projects:5000/projects/{userID}/{projectID}")
        project = response.json() if response.ok else []

        response1 = requests.get(f"HTTP://projects:5000/projects/{userID}")
        projects = response1.json() if response1.ok else []

        response2 = requests.get(f"HTTP://palettes:5000/palettes/{userID}")
        palettes = response2.json() if response2.ok else[]
        return render_template("projectPage.html",
                        navBarTheme = "/static/CSS/mainPageFall.css",
                        mainTheme = "/static/CSS/navBarFall.css",
                        theme = "Fall Theme",
                        projectTitle = project["title"],
                        palettes = palettes,
                        hookSize = "none added",
                        yarn = "none added",
                        pattern = "none added",
                        counters = project["counters"],
                        projects = projects,
                        project = project)
    else:
        return redirect(url_for('frontpage'))


@app.route('/saveProject/<int:projectID>', methods=['POST'])
def saveProject(projectID: int):
    if userLoggedIn():
        userID = session["userID"]
        date_ = date.today().isoformat()
        title = request.form["title"]
        hookSize = request.form.get("needle", default="")
        yarn = request.form.get("yarn", default="")
        pattern = request.form.get("pattern", default="")
        paletteID = request.form.get("paletteOp", default=None)

        payload = {"projectID": projectID, "userID": userID,
                   "date": date_, "title": title, "hookSize": hookSize,
                   "yarn":yarn, "pattern": pattern, "paletteID": paletteID}
        response = requests.post('HTTP://projects:5000/saveProject', json=payload)
        project = response.json() if response.ok else []

        return redirect(url_for('project', projectID=project["id"]))
    else:
        return redirect(url_for('frontpage'))


@app.route('/archiveProject/<int:projectID>', methods=["POST"])
def archiveProject(projectID: int):
    if userLoggedIn():
        date_ = date.today().isoformat()

        payload = {"projectID": projectID, "date": date_}
        requests.post("HTTP://projects:5000/archiveProject", json = payload)
        return redirect(url_for('archive'))
    else:
        return redirect(url_for('frontpage'))


# render archive page
@app.route('/archive', methods=['POST', 'GET'])
def archive():
    if userLoggedIn():
        userID = session["userID"]
        response1 = requests.get(f"HTTP://projects:5000/projects/{userID}")
        projects = response1.json() if response1.ok else []

        return render_template("archive.html", 
                            projects = projects )
    else:
        return redirect(url_for('frontpage'))


#################
#   counters    #
##################################################################

@app.route('/newCounter/<int:projectID>', methods=['POST', 'GET'])
def newCounter(projectID: int):
    requests.get(f"HTTP://projects:5000/newCounter/{projectID}")
    return redirect(url_for('project', projectID = projectID))

@app.route('/upCounter/<int:projectID>/<int:counterID>', methods=['POST', 'GET'])
def upCounter(projectID: int, counterID: int):
    requests.get(f"HTTP://projects:5000/upCounter/{projectID}/{counterID}")
    return redirect(url_for('project', projectID = projectID))

@app.route('/downCounter/<int:projectID>/<int:counterID>', methods=['POST', 'GET'])
def downCounter(projectID: int, counterID: int):
    requests.get(f"HTTP://projects:5000/downCounter/{projectID}/{counterID}")
    return redirect(url_for('project', projectID = projectID))

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
    requests.post('HTTP://users:5000/register', json = user)
    return redirect(url_for("frontpage"))


# we need to remove the logic and keep the render template
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    payload = {"username":username, "password":password}
    response = requests.post('HTTP://users:5000/login', json = payload)
    user = response.json() if response.ok else None
    if user:
        session["userID"] = user["id"]
        return redirect(url_for('profile'))
    else:
        return redirect(url_for('frontpage'))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("frontpage"))
