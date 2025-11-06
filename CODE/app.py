from datetime import datetime, timedelta

from flask import Flask, make_response, redirect, render_template, request

app = Flask(__name__)

@app.route("/")
def theme():
    theme = request.cookies.get("theme", "fall")
    if theme == "light":
        return render_template("app.html",
                            navBarTheme = "/app/static/CSS/navBarLight.css",
                            mainTheme = "/app/static/CSS/mainPageLight.css")
    if theme == "fall":
        return render_template("app.html",
                            navBarTheme = "/app/static/CSS/navBar.css",
                            mainTheme = "/app/static/CSS/mainPage.css")


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
