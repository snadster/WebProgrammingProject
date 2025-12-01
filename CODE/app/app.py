from datetime import datetime, timedelta

from flask import make_response, redirect, render_template, request, url_for

from main import app
from pythonFiles.user import User

@app.route("/")
def frontpage():
    return render_template("frontPage.html")

@app.route("/profile")
def profile():
    return render_template("profile.html", 
                           Username = "User.username",
                           mail = "User.mail",)

@app.route("/project")
def project():
    return render_template("projectPage.html")


@app.route("/register", methods=["POST"])
def register():
    username = request.form["username"]
    password = request.form["password"]
    email = request.form["mail"]
    user = User(username, password, email)
    user.save()
    return redirect(url_for("profile"))


def theme():
    theme = request.cookies.get("theme", "fall")
    if theme == "light":
        return render_template("frontPage.html",
                            navBarTheme = "/static/CSS/mainPageLight.css",
                            mainTheme = "/static/CSS/navBarLight.css",
                            theme = "Pastel Theme")
    else:
        return render_template("frontPage.html",
                            navBarTheme = "/static/CSS/navBarFall.css",
                            mainTheme = "/static/CSS/mainPageFall.css",
                            theme = "Fall Theme")

# change from switch to selected theme if want more than two themes

@app.route("/clicked")
def theme2():
    theme = request.cookies.get("theme", "fall")
    response = make_response(redirect('/'))
    if theme == "light":
        response.set_cookie('theme', "fall",
                            expires=datetime.now() + timedelta(days=30))
    else:
        response.set_cookie('theme', "light",
                            expires=datetime.now() + timedelta(days=30))
    return response
