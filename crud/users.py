from sqlalchemy import select

from db import Session
from models import User


def create(user: User):
    with Session.begin() as session:
        try:
            session.add(user)
        except:
            return False
        return True


def get_by_id(id: int):
    with Session.begin() as session:
        user_select = select(User).where(User.id == id)
        user = session.scalar(user_select)
        return user


def get_all():
    with Session.begin() as session:
        user_select = select(User)
        return session.scalars(user_select).all()


def find_user(user: User):
    with Session.begin() as session:
        user_select = select(User).where(
            User.name == user.name, User.password == user.password
        )
        user_in_db = session.scalar(user_select)
        return user_in_db


def update(id: int, new_user: User):
    with Session.begin() as session:
        user_select = select(User).where(User.id == id)
        user = session.scalar(user_select)
        if user == None:
            return False
        for key, value in new_user.__dict__.items():
            if key != "id" and key != "_sa_instance_state" and value is not None:
                setattr(user, key, value)
        return user


def delete(id: int):
    with Session.begin() as session:
        user_select = select(User).where(User.id == id)
        user = session.scalar(user_select)
        if user == None:
            return False
        session.delete(user)
        return True
