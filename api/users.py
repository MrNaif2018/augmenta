from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import crud.users as users

router = APIRouter()


class User(BaseModel):
    name: str
    email: str


class UserIn(User):
    password: str


@router.get("/all", response_model=list[User])
def get_all_users():
    return users.get_all()


@router.get("/{id}", response_model=User)
def get_user(id: int):
    user = users.get_by_id(id)
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.get("/check", response_model=User)
def check_user(user: UserIn):
    user = users.find_user(user)
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


@router.post("/add", response_model=User)
def add_user(user: UserIn):
    if users.create(user):
        return users.find_user(user)
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Such a user already exists"
    )


@router.patch("/update", response_model=User)
def update_user(user: UserIn):
    users.update(user)
    return users.find_user(user)


@router.delete("/delete")
def delete_user(id: int):
    if not users.delete(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return JSONResponse(
        content={"message": "The user has been successfully deleted"},
        status_code=status.HTTP_200_OK,
    )
