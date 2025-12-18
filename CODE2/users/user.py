from __future__ import annotations

from flask_login import UserMixin
from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column

from database import db

# this should by and large work.

class User(db.Model, UserMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, init=False) #maybe init=false
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    mail: Mapped[str] = mapped_column()

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_by_username(username: str) -> User | None:
        return db.session.scalar(select(User).filter_by(username=username))

    @staticmethod
    def get_by_id(user_id: int) -> User | None:
        return db.session.get(User, user_id)
