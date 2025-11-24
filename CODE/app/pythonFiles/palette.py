from sqlalchemy.orm import Mapped, mapped_column

from main import db

class Palette(db.Model):
    __tablename__ = "palette"

    id: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column() # palette title
    color1: Mapped[str | None] = mapped_column()
    color2: Mapped[str | None] = mapped_column()
    color3: Mapped[str | None] = mapped_column()
    color4: Mapped[str | None] = mapped_column()
    color5: Mapped[str | None] = mapped_column()
    color6: Mapped[str | None] = mapped_column()
    color7: Mapped[str | None] = mapped_column()
    color8: Mapped[str | None] = mapped_column()

    # might be static might not. only god knows tbh.
    def newPalette():
        count = 0
        Palette.id = count +1
        count = count+1
        Palette.name = "New Palette"
        Palette.color1 = None 
        Palette.color2 = None
        Palette.color3 = None
        Palette.color4 = None
        Palette.color5 = None
        Palette.color6 = None
        Palette.color7 = None
        Palette.color8 = None

    def addColor(slot, color): #slot is the color[int] and color is the hex code
        Palette.slot = color 
        return

    def deleteColor(slot):
        Palette.slot = None
        return