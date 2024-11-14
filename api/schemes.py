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

    model_config = ConfigDict(from_attributes=True)


class UpdateRequest(CreateRequest):
    pass


class DisplayRequest(CreateRequest):
    id: str


class LookupParams(BaseModel):
    name: str
