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
    id: int


class CreateRequest(BaseModel):
    user_id: int
    name: str
    logo: str
    short_descr: str
    sites: list[str]
    contacts: list[str]
    socnets: list[str]
    int_facts: list[str]
    short_hist: str
    partners: list[str]
    capital: str
    ownership: str
    jurisdiction: str
    products: list[str]
    products_info: list[str]
    products_logo: list[str]
    employees_num: int
    management: list[str]
    branches: list[str]

    model_config = ConfigDict(from_attributes=True)


class UpdateRequest(CreateRequest):
    pass


class DisplayRequest(CreateRequest):
    id: int
