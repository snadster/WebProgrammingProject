from __future__ import annotations #magic, fixes problems (changes how python sees code)

from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date  # use this to get todays date

from pythonFiles.database import db
from pythonFiles.counter import Counter
from pythonFiles.palette import Palette
from pythonFiles.project_to_palette import project_to_palette_table
import pythonFiles.user


class Project(db.Model):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True, init=False) #maybe init=false
    user: Mapped[str] = mapped_column(unique=True) # somehow connect to actual user
    date: Mapped[date] = mapped_column() #how do this
    title: Mapped[str] = mapped_column(default="New Project")
    archived: Mapped[bool] = mapped_column(default=False)
    counters: Mapped[list[Counter] | None] = relationship(default_factory=list) #relationship is magic, this one connects a table of counters to a project
    notes: Mapped[str | None] = mapped_column(default=None)
    hookSize: Mapped[float | None] = mapped_column(default=None)
    yarn: Mapped[str | None] = mapped_column(default=None)
    pattern: Mapped[str | None] = mapped_column(default=None)
    palette: Mapped[list[Palette]] = relationship(secondary=project_to_palette_table,
                                                  default_factory=list)

#################
#   Functions   #
#################

def save(self):
    db.session.add(self)
    db.session.commit()


#########################
## things we maybe need:
## - addCounter() here or elsewhere? currently in counter