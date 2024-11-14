from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from api.db import db


class User(db.Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    password: Mapped[str]

    def __repr__(self):
        return f"UserBase(id={self.id}, name={self.name}, email={self.email}, password={self.password})"


class Request(db.Base):
    __tablename__ = "requests"

    id: Mapped[str] = mapped_column(primary_key=True)
    data = mapped_column(JSON)
