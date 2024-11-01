from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

from api import models, schemes


def create(user: schemes.CreateUser):
    try:
        obj = models.User(**user.model_dump())
        obj.save()
        return obj
    except IntegrityError as e:
        raise HTTPException(422, str(e.orig))


def get_by_id(model_id: int, raise_exception=True):
    model = models.User.query.where(models.User.id == model_id).first()
    if model is None and raise_exception:
        raise HTTPException(404, f"{models.User.__name__} with id {model_id} not found")
    return model


def get_all():
    return models.User.query.all()


def update(user: models.User, new_user: schemes.User):
    user.update(**new_user.model_dump(exclude_unset=True))
    user.save()
    return user


def delete(model_id: int):
    user = get_by_id(model_id)
    user.delete()
    return user
