
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date # use this to get todays date

from main import db
import counter
import user

class Project(db.Model):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True) #maybe init=false
    user: Mapped[str] = mapped_column(unique=True) # somehow connect to actual user
    title: Mapped[str] = mapped_column(init=False)
    archived: Mapped[bool] = mapped_column()
    date: Mapped[str] = mapped_column(init=False) # maybe make dateType + connect to actual date
    counters: Mapped[int] = mapped_column(init=False) #make own class for these
    hookSize: Mapped[float | None] = mapped_column(init=False)
    yarn: Mapped[str | None] = mapped_column()
    pattern: Mapped[str | None] = mapped_column()
    palette: Mapped[str | None] = mapped_column() # for name of? how do this.

    @staticmethod 
    # should maybe return something? 
    # is for creating a new project in the database
    def newProject(user):
        counter = 0
        Project.id = counter+1
        count = count+1
        Project.user == user
        Project.title == "New Project!"
        Project.archived == False
        Project.date == date.today
        Project.counters == 0
        Project.hookSize == None
        Project.yarn == None 
        Project.pattern == None
        Project.palette == None
        return # idfk. 

    @staticmethod # this one doesnt work. Bc I am dumb.
    def changeTitle(id, title):
        if Project.id == id:
            Project.title = title
        else:
            pass

#########################
## things we maybe need:
## - what do we do with the rest of it I'm dumb 
## - addCounter() here or elsewhere? currently in counter