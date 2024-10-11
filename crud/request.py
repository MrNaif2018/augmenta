from sqlalchemy import select

from db import Session
from models import Request


def create(request: Request):
    with Session.begin() as session:
        try:
            session.add(request)
        except Exception:
            return False
        return True


def get_by_id(id: int):
    with Session.begin() as session:
        request_select = select(Request).where(Request.id == id)
        request = session.scalar(request_select)
        return request


def get_by_user_id(user_id: int):
    with Session.begin() as session:
        request_select = select(Request).where(Request.user_id == user_id)
        request = session.scalar(request_select)
        return request


def update(new_request: Request):
    with Session.begin() as session:
        session.merge(new_request)


def delete(id: int):
    with Session.begin() as session:
        request_select = select(Request).where(Request.id == id)
        request = session.scalar(request_select)
        if request == None:
            return False
        session.delete(request)
        return True
