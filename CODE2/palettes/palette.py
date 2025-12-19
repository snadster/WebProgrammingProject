from sqlalchemy.orm import Mapped, mapped_column

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

    def toDict(self):
        return {"id": self.id, "userID": self.userID, "name": self.name,
                "color1": self.color1, "color2": self.color2,
                "color3": self.color3, "color4": self.color4,
                "color5": self.color5, "color6": self.color6,
                "color7": self.color7, "color8": self.color8}

    def deletePalette(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.add(self)
        db.session.commit()
