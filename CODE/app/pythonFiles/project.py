from __future__ import annotations #magic, fixes problems (changes how python sees code)

from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date  # use this to get todays date

from main import db
from counter import Counter
from palette import Palette
from project_to_palette import project_to_palette_table
import user

class Project(db.Model):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True) #maybe init=false
    user: Mapped[str] = mapped_column(unique=True) # somehow connect to actual user
    date: Mapped[date] = mapped_column()
    title: Mapped[str] = mapped_column(default="New Project")
    archived: Mapped[bool] = mapped_column(default=False)
    counters: Mapped[list[Counter]] = relationship(default_factory=list) #relationship is magic
    hookSize: Mapped[float | None] = mapped_column(default=None)
    yarn: Mapped[str | None] = mapped_column(default=None)
    pattern: Mapped[str | None] = mapped_column(default=None)
    palette: Mapped[list[Palette]] = relationship(secondary=project_to_palette_table,
                                                  default_factory=list)

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