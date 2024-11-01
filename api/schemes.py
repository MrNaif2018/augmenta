from pydantic import BaseModel, ConfigDict, EmailStr

# class CreateUser(BaseModel):
#     name: str
#     email: str
#     password: str


# class User(BaseModel):
#     name: str
#     email: str

#     model_config = ConfigDict(from_attributes=True, extra="ignore")


# class UserIn(User):
#     password: str


class BaseUser(BaseModel):
    email: EmailStr
    name: str

    model_config = ConfigDict(from_attributes=True)


class CreateUser(BaseUser):
    password: str


class User(BaseUser):
    password: str


class DisplayUser(BaseUser):
    id: int
