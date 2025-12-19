from __future__ import annotations #magic, fixes problems (changes how python sees code)

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date  # use this to get todays date

from database import db
from counter import Counter

class Project(db.Model):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True, init=False) #maybe init=false
    userID: Mapped[int] = mapped_column()
    date: Mapped[date] = mapped_column() #how do this
    title: Mapped[str] = mapped_column(default="New Project")
    archived: Mapped[bool] = mapped_column(default=False)
    counters: Mapped[list[Counter] | None] = relationship(default_factory=list) #relationship is magic, this one connects a table of counters to a project
    # notes: Mapped[list[str] | None] = mapped_column(default=None)
    hookSize: Mapped[str | None] = mapped_column(default=None)
    yarn: Mapped[str | None] = mapped_column(default=None)
    pattern: Mapped[str | None] = mapped_column(default=None)
    paletteID: Mapped[int | None] = mapped_column(default=None)

    #################
    #    Methods    #
    #################

    def toDict(self):
        return {"id": self.id, "userID": self.userID, "date": self.date,
                "title": self.title, "archived": self.archived,
                "counters": self.counters, "hookSize": self.hookSize,
                "yarn": self.yarn, "pattern": self.pattern,
                "paletteID": self.paletteID}

    def save(self):
        db.session.add(self)
        db.session.commit()
