from sqlalchemy.orm import Mapped, mapped_column

from main import db

class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True) #maybe init=false
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()

    
    def login(self):
        pass

    def save_user(username, password):
        count = 0
        User.id = count+1
        count = count+1
        User.username = username
        User.password = password

    
