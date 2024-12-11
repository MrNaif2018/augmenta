from datetime import datetime

from sqlalchemy import ARRAY, JSON, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from api.db import db


class User(db.Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    password: Mapped[str]

    def __repr__(self):  # pragma: no cover
        return f"UserBase(id={self.id}, name={self.name}, email={self.email}, password={self.password})"


class Request(db.Base):
    __tablename__ = "requests"

    id: Mapped[str] = mapped_column(primary_key=True)
    data = mapped_column(JSON)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=True)
    created: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Token(db.Base):
    __tablename__ = "tokens"

    id: Mapped[str] = mapped_column(primary_key=True)
    scopes: Mapped[list[str]] = mapped_column(ARRAY(Text))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
