from sqlalchemy.orm import Mapped, mapped_column

from main import db

class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, init=False) #maybe init=false
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    mail: Mapped[str] = mapped_column()

    def save(self):
        db.session.add(self)
        db.session.commit()
