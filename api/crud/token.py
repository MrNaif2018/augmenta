import secrets

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from api import models


def create(token_data: dict):
    try:
        token_data["id"] = secrets.token_urlsafe()
        obj = models.Token(**token_data)
        obj.save()
        return obj
    except IntegrityError as e:
        raise HTTPException(422, str(e.orig))
