from fastapi_sqlalchemy import ModelBase, SQLAlchemy
from sqlalchemy import ARRAY, ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from api.db import db

# class Base(db.Base):
#     pass


class User(db.Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    password: Mapped[str]

    def __repr__(self):
        return f"UserBase(id={self.id}, name={self.name}, email={self.email}, password={self.password})"


class Request(db.Base):
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    name: Mapped[str]
    logo: Mapped[str]
    short_descr: Mapped[str]
    sites: Mapped[list[str]] = mapped_column(ARRAY(String))
    contacts: Mapped[list[str]] = mapped_column(ARRAY(String))
    socnets: Mapped[list[str]] = mapped_column(ARRAY(String))
    int_facts: Mapped[list[str]] = mapped_column(ARRAY(String))
    short_hist: Mapped[str]
    partners: Mapped[list[str]] = mapped_column(ARRAY(String))
    capital: Mapped[str]
    ownership: Mapped[str]
    jurisdiction: Mapped[str]
    products: Mapped[list[str]] = mapped_column(ARRAY(String))
    products_info: Mapped[list[str]] = mapped_column(ARRAY(String))
    products_logo: Mapped[list[str]] = mapped_column(ARRAY(String))
    employees_num: Mapped[int | None]
    management: Mapped[list[str]] = mapped_column(ARRAY(String))
    branches: Mapped[list[str]] = mapped_column(ARRAY(String))
