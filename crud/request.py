from sqlalchemy import select

from db import Session
from models import Request


def create(request: Request):
    with Session.begin() as session:
        session.add(request)


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


def update(id: int, new_request: Request):
    with Session.begin() as session:
        request_select = select(Request).where(Request.id == id)
        request = session.scalar(request_select)
        if request == None:
            return False
        for key, value in new_request.__dict__.items():
            if key != "id" and key != "_sa_instance_state" and value is not None:
                setattr(request, key, value)
        return request


def delete(id: int):
    with Session.begin() as session:
        request_select = select(Request).where(Request.id == id)
        request = session.scalar(request_select)
        if request == None:
            return False
        session.delete(request)
        return True
