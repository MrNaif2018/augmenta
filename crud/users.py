from sqlalchemy import select

from db import Session
from models import User


def create_user(user: User):
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
