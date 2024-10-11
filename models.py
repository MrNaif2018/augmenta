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
    contacts: Mapped[list[str]]
    socnets: Mapped[list[str]]
    int_facts: Mapped[str]
    short_hist: Mapped[str]
    partners: Mapped[list[str]]
    capital: Mapped[str]
    ownership: Mapped[str]
    jurisdiction: Mapped[str]
    products: Mapped[list[str]]
    products_info: Mapped[list[str]]
    products_logo: Mapped[list[str]]
    employees_num: Mapped[list[str]]
    management: Mapped[list[str]]
    branches: Mapped[list[str]]
