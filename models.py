from typing import List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str]
    password: Mapped[str]

    def __repr__(self):
        return f"UserBase(id={self.id}, name={self.name}, email={self.email}, password={self.password})"


class Request(Base):
    __tablename__ = "requests"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id))
    logo: Mapped[str]
    short_descr: Mapped[str]
    sites: Mapped[str]
    contacts: Mapped[List[str]]
    socnets: Mapped[List[str]]
    int_facts: Mapped[str]
    short_hist: Mapped[str]
    partners: Mapped[List[str]]
    capital: Mapped[str]
    ownership: Mapped[str]
    jurisdiction: Mapped[str]
    products: Mapped[List[str]]
    products_info: Mapped[List[str]]
    products_logo: Mapped[List[str]]
    employees_num: Mapped[List[str]]
    management: Mapped[List[str]]
    branches: Mapped[List[str]]
