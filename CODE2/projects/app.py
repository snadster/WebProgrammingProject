from datetime import date

from flask import Flask, jsonify, request
from sqlalchemy import select

import database
from database import db
from project import Project
from counter import Counter


# Start flask
app = Flask(__name__)
app.secret_key = "secret"

# Database stuff
database.init_db(app, "sqlite:///database.db")
database.setup_db(app)


#############
#   ROUTES  #
#############################################################################


#################
#   PROJECT     #
#############################################################################


@app.route('/newProject', methods=["POST"])
def newProject():
    userID = request.json["userID"]
    date_ = date.today()
    title = "My New Project!"
    archived = False
    counters = []
    hookSize = None
    yarn = None
    pattern = None
    paletteID = None
    project = Project(userID, date_, title, archived, 
                      counters, hookSize, yarn, pattern, 
                      paletteID)
    project.save()
    return jsonify(project.toDict())


# save the project to database with user input
# make the ID the one it gets from makeProject
@app.route('/saveProject', methods=['POST'])
def saveProject():
    data = request.json
    project = db.session.get(Project, data["projectID"])
    project.userID = data["userID"]
    project.date_ = date.fromisoformat(data["date"])
    project.title = data["title"]
    project.hookSize = data["hookSize"]
    project.yarn = data["yarn"]
    project.pattern = data["pattern"]
    project.paletteID = data["paletteID"]
    project.save()
    return jsonify(project.toDict())


@app.route('/archiveProject', methods=['POST'])
def archiveProject():
    data = request.json
    project = db.session.get(Project, data["projectID"])
    project.date_ = data["date"]  # VALUE WE CHANGE
    project.archived = True # VALUE WE CHANGE
    project.save()
    return {"ok": True}


# all projects for this user
@app.route('/projects/<int:userID>', methods=['GET'])
def getProjects(userID: int):
    projects = db.session.scalars(select(Project).where(Project.userID == userID)).all()
    return [project.toDict() for project in projects]


# singluar project based on its id
@app.route('/projects/<int:userID>/<int:projectID>', methods=['GET'])
def projectByID(userID: int, projectID: int):
    project = db.session.get(Project, projectID)
    if project.userID == userID:
        return project.toDict()
    else:
        return {}, 404


# all counters for one project
@app.route('/projects/<int:userID>/<int:projectID>/counters', methods=['GET'])
def getCounters(userID: int, projectID: int):
    project = db.session.get(Project, projectID)
    if project.userID == userID:
        return [counter.toDict() for counter in project.counters]
    else:
        return {}, 404


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
    project.save()
    return {"ok": True}


# add to counter and minus from counter. 
# Yes they're basically the same code, no I couldn't 
# as of this moment bother putting them into one function
@app.route('/upCounter/<int:projectID>/<int:counterID>', methods=['POST', 'GET'])
def upCounter(counterID: int, projectID: int):
    counter = db.session.get(Counter, counterID)
    counter.value = counter.value + 1
    counter.save()
    return {"ok": True}


@app.route('/downCounter/<int:projectID>/<int:counterID>', methods=['POST', 'GET'])
def downCounter(counterID: int, projectID: int):
    counter = db.session.get(Counter, counterID)
    counter.value = counter.value - 1
    counter.save()
    return {"ok": True}
