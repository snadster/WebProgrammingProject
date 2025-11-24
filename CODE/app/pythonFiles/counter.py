from sqlalchemy.orm import Mapped, mapped_column

from main import db

class Counter(db.Model):
    __tablename__ = "counter"

    id: Mapped[int] = mapped_column(primary_key=True) #maybe init=false
    type: Mapped[str] = mapped_column() # three types? normal, loop, connected to loop?
    value: Mapped[int] = mapped_column()
    loop: Mapped[int | None ] = mapped_column()


    @staticmethod
    def addCounter(typ):
        count = 0
        Counter.id = count+1
        count = count+1
        Counter.type = typ
        Counter.value = 0
        Counter.loop = None
        