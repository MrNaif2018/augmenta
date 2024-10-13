from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

import crud.users as users

router = APIRouter()


class UserIn(BaseModel):
    name: str
    email: str
    password: str


class UserOut(BaseModel):
    name: str
    email: str


@router.get("/all", response_model=List[UserOut])
def get_all_users():
    return users.get_all()


@router.get("/{id}")
def get_user(id: int):
    user = users.get_by_id(id)
    if user == None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
