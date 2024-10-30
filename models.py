from typing import List

from sqlalchemy import ARRAY, ForeignKey, String
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
    contacts: Mapped[List[str]] = mapped_column(ARRAY(String))
    socnets: Mapped[List[str]] = mapped_column(ARRAY(String))
    int_facts: Mapped[str]
    short_hist: Mapped[str]
    partners: Mapped[List[str]] = mapped_column(ARRAY(String))
    capital: Mapped[str]
    ownership: Mapped[str]
    jurisdiction: Mapped[str]
    products: Mapped[List[str]] = mapped_column(ARRAY(String))
    products_info: Mapped[List[str]] = mapped_column(ARRAY(String))
    products_logo: Mapped[List[str]] = mapped_column(ARRAY(String))
    employees_num: Mapped[List[str]] = mapped_column(ARRAY(String))
    management: Mapped[List[str]] = mapped_column(ARRAY(String))
    branches: Mapped[List[str]] = mapped_column(ARRAY(String))
