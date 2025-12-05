from datetime import datetime, timedelta

from flask import make_response, redirect, render_template, request, url_for

from main import app
from pythonFiles.user import User
from pythonFiles.project import Project

# front page 
@app.route("/")
def frontpage():
    return render_template("frontPage.html")


@app.route("/login")
def login(self):
    bool1 = self.username == User.username
    bool2 = self.password == User.password
    if (bool1 & bool2): #somehow check if user exists.
        return redirect(url_for("profile"))
    else:   # does a way exist to make a pop-up on the login modal? probably. But this is a MVP
        return redirect(url_for("frontpage"))

@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    email = request.form["mail"]
    user = User(username, password, email)
    user.save()
    return redirect(url_for("profile"))


@app.route("/profile")
def profile():
    return render_template("profile.html", 
                           Username = User.username,
                           mail = User.mail)

# project itself (it has a theme cookie)
# btw we need to redirect to correct project by checking
# which one they requested (somehow)
# maybe ask for the ID associated with the one they clicked (from db),
# and then pull the information belonging to that one.
@app.route("/project")
def project():
    theme = request.cookies.get("theme", "fall")
    if theme == "light":
        return render_template("projectPage.html", 
                                navBarTheme = "/static/CSS/mainPageLight.css",
                                mainTheme = "/static/CSS/navBarLight.css",
                                theme = "Pastel Theme",
                                projectTitle = Project.title,
                                projectID = Project.id)
    else:
        return render_template("projectPage.html",
                            navBarTheme = "/static/CSS/navBarFall.css",
                            mainTheme = "/static/CSS/mainPageFall.css",
                            theme = "Fall Theme")

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


# color palettes
@app.route("/palettes")
def palettes():
    return render_template("colorPalettes.html")

@app.route("/newPalette")
def newPalette():
    return render_template("makePalette.html")


# dev notes
@app.route("/devNotes")
def devNotes():
    return render_template("DevNotes.html")