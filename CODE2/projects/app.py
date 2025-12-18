
from flask import Flask, session

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

import database
from database import db

import requests
# Start flask
app = Flask(__name__)
app.secret_key = "secret"

# Database stuff
database.init_db(app, "sqlite:///database.db")
database.setup_db(app)


#############
#   ROUTES  #
#############################################################################

from datetime import date, datetime, timedelta
from flask import jsonify, make_response, redirect, request, url_for
from sqlalchemy import select
from database import db

from project import Project
from counter import Counter

#################
#   PROJECT     #
#############################################################################

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


@app.route('/newProject')
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
    response2 = requests.get("HTTP://palettes:5000/database")
    palettes = response2.json() if response2.ok else[]

    project = Project(user, date_, title, archived, 
                      counters, hookSize, yarn, pattern, 
                      palettes)
    project.save()
    # my version of trying to get the project id
    return jsonify([{
                "id": p.id, "user_id": p.user_id,
                "user": p.user, "date": p.date,
                "title": p.title, "archived": p.archived,
                "counters": p.counters, "hookSize": p.hookSize,
                "yarn": p.yarn, "pattern": p.pattern,
                "palette": p.palette} 
                for p in project])


# save the project to database with user input
# make the ID the one it gets from makeProject
@app.route('/saveProject', methods=['POST', 'GET'])
def saveProject():
    data = request.form
    project = db.session.get(Project, data.projectID)
    project.user = current_user._get_current_object()
    project.date_ = date.today()
    project.title = data["title"]
    project.archived = False
    project.counters = []
    # project.notes = request.form.get("notes", default=[])
    project.hookSize = data["hookSize"]
    project.yarn = data["yarn"]
    project.pattern = data["pattern"]
    project.palette = data["palette"]
    project.save()
    return jsonify([{
                "id": p.id, "user_id": p.user_id,
                "user": p.user, "date": p.date,
                "title": p.title, "archived": p.archived,
                "counters": p.counters, "hookSize": p.hookSize,
                "yarn": p.yarn, "pattern": p.pattern,
                "palette": p.palette} 
                for p in project])


@app.route('/archiveProject', methods=['POST', 'GET'])
def archiveProject():
    projectID = request.form
    project = db.session.get(Project, projectID["projectID"])
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
    return jsonify([{
                "id": p.id, "user_id": p.user_id,
                "user": p.user, "date": p.date,
                "title": p.title, "archived": p.archived,
                "counters": p.counters, "hookSize": p.hookSize,
                "yarn": p.yarn, "pattern": p.pattern,
                "palette": p.palette} 
                for p in project])


# all projects for this user
@app.route('/database', methods=['GET'])
def getProjects():
    project = db.session.scalars(select(Project).where(Project.user_id == session.keys())).all()
    return jsonify([{
                "id": p.id, "user_id": p.user_id,
                "date": p.date,
                "title": p.title, "archived": p.archived,
                "counters": p.counters, "hookSize": p.hookSize,
                "yarn": p.yarn, "pattern": p.pattern,
                "palette": p.palette} 
                for p in project])

# singluar project based on its id
@app.route('/database/<int:projectID>', methods=['GET'])
def projectByID(projectID: int):
    project = db.session.scalars(select(Project).where(Project.id == projectID)).all()
    return jsonify([{
                "id": p.id, "user_id": p.user_id, 
                "date": p.date,
                "title": p.title, "archived": p.archived,
                "counters": p.counters, "hookSize": p.hookSize,
                "yarn": p.yarn, "pattern": p.pattern,
                "palette": p.palette} 
                for p in project])


# all counters for one project
@app.route('/database/counter', methods=['GET'])
def getCounters():
    counter = db.session.scalars(select(Counter)).all()
    return jsonify([{
                "id": c.id, "value": c.value,
                "link": c.link, "loop": c.loop,
                "project": c.project} 
                for c in counter])


#################
#   COUNTERS    #
##################################################################
# TODO FIX THE RETURNS ON THIS
@app.route('/newCounter/<int:projectID>', methods=['POST', 'GET'])
def newCounter(projectID: int):
    project = db.session.get(Project, projectID)
    value = 0
    counter = Counter(value, None, None, projectID)
    counter.save()
    project.counters.append(counter)
    return redirect(url_for('project',  projectID=projectID))

# add to counter and minus from counter. 
# Yes they're basically the same code, no I couldn't 
# as of this moment bother putting them into one function
@app.route('/upCounter/<int:projectID>/<int:counterID>', methods=['POST', 'GET'])
def upCounter(counterID: int, projectID: int):
    counter = db.session.get(Counter, counterID)
    counter.id = counterID
    counter.value = counter.value+1
    counter.link = None
    counter.loop = None
    counter.save()
    return redirect(url_for('project',  projectID=projectID))

@app.route('/downCounter/<int:projectID>/<int:counterID>', methods=['POST', 'GET'])
def downCounter(counterID: int, projectID: int):
    counter = db.session.get(Counter, counterID)
    counter.id = counterID
    counter.value = counter.value-1
    counter.link = None
    counter.loop = None
    counter.save()
    return redirect(url_for('project',  projectID=projectID))

#################
#   palettes    #
##################################################
