from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from pythonFiles.database import db

class Counter(db.Model):
    __tablename__ = "counter"

    id: Mapped[int] = mapped_column(primary_key=True, init=False) #maybe init=false
    value: Mapped[int] = mapped_column()
    link: Mapped[int | None] = mapped_column(ForeignKey("counter.id")) # int is id of linked counter
    loop: Mapped[int | None] = mapped_column()
    project: Mapped[int] = mapped_column(ForeignKey("project.id")) # the project it belongs to, hopefully


    