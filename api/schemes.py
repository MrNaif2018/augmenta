from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class BaseUser(BaseModel):
    email: EmailStr
    name: str

    model_config = ConfigDict(from_attributes=True)


class CreateUser(BaseUser):
    password: str


class User(BaseUser):
    password: str


class DisplayUser(BaseUser):
    id: str


class CreateRequest(BaseModel):
    data: dict
    user_id: str | None = None

    model_config = ConfigDict(from_attributes=True)


class UpdateRequest(CreateRequest):
    pass


class DisplayRequest(CreateRequest):
    id: str
    created: datetime


class LookupParams(BaseModel):
    name: str


class CreateToken(BaseModel):
    email: EmailStr
    password: str
    scopes: list[str]


class DisplayToken(BaseModel):
    id: str
    user_id: str
    scopes: list[str]
