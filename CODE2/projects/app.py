
from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass

import database
from database import db

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
from flask_login import current_user, login_required
from sqlalchemy import select
from database import db

# TODO
# not allowed to import from microservices. Do https gets. FIX EVERYWHERE.

#################
#   PROJECT     #
#############################################################################

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
    # my version of trying to get the project id
    projectID = project.id
    return redirect(url_for('makeProject',  projectID=projectID))

# save the project to database with user input
# make the ID the one it gets from makeProject
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

#######################################
##  ACTUAL CORRRECT ROUTE I THINK     #
#######################################
# TODO
## db

# all projects for this user
@app.route('/database', methods=['GET'])
def getProjects():
    project = db.session.scalars(select(Project).where(Project.user == current_user)).all()
    return jsonify([{
                "id": p.id, "user_id": p.user_id,
                "user": p.user, "date": p.date,
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
                "user": p.user, "date": p.date,
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
