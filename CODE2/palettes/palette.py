from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Engine, ForeignKey


from database import db

class Palette(db.Model):
    __tablename__ = "palette"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    userID: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column() # palette title
    color1: Mapped[str | None] = mapped_column() #hopefully a hex or rgb but idk yet
    color2: Mapped[str | None] = mapped_column()
    color3: Mapped[str | None] = mapped_column()
    color4: Mapped[str | None] = mapped_column()
    color5: Mapped[str | None] = mapped_column()
    color6: Mapped[str | None] = mapped_column()
    color7: Mapped[str | None] = mapped_column()
    color8: Mapped[str | None] = mapped_column()


    def deletePalette(self):
        db.metadata.drop_all(self)

    def save(self):
        db.session.add(self)
        db.session.commit()
