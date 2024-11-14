from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from ulid import ULID

from api import models, schemes


def create(data: schemes.CreateRequest):
    try:
        data = data.model_dump()
        data["id"] = str(ULID())
        obj = models.Request(**data)
        obj.save()
        return obj
    except IntegrityError as e:
        raise HTTPException(422, str(e.orig))


def get_by_id(model_id: int, raise_exception=True):
    model = models.Request.query.where(models.Request.id == model_id).first()
    if model is None and raise_exception:
        raise HTTPException(404, f"{models.Request.__name__} with id {model_id} not found")
    return model


def get_all():
    return models.Request.query.all()


def update(obj: models.Request, new_obj: schemes.UpdateRequest):
    obj.update(**new_obj.model_dump(exclude_unset=True))
    obj.save()
    return obj


def delete(model_id: int):
    obj = get_by_id(model_id)
    obj.delete()
    return obj
