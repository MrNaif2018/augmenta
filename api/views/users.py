from fastapi import APIRouter

from api import crud, schemes, utils

# from api.db import get_db

router = APIRouter()


@router.post("", response_model=schemes.DisplayUser)
async def create_user(user: schemes.CreateUser):
    return crud.users.create(user)


@router.patch("/{model_id}", response_model=schemes.DisplayUser)
def update_user(model_id: str, data: utils.to_optional(schemes.User)):
    user = crud.users.get_by_id(model_id)
    return crud.users.update(user, data)


@router.get("", response_model=list[schemes.DisplayUser])
def get_all_users():
    return crud.users.get_all()


@router.get("/{model_id}", response_model=schemes.DisplayUser)
def get_user(model_id: str):
    return crud.users.get_by_id(model_id)


@router.delete("/{model_id}", response_model=schemes.DisplayUser)
def delete_user(model_id: str):
    return crud.users.delete(model_id)
