from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

import crud.request as requests

router = APIRouter()


class Request(BaseModel):
    logo: str
    short_descr: str
    sites: list[str]
    contacts: list[str]
    socnets: list[str]
    int_facts: str
    short_hist: str
    partners: list[str]
    capital: str
    ownership: str
    jurisdiction: str
    products: list[str]
    products_info: list[str]
    products_logo: list[str]
    employees_num: list[str]
    management: list[str]
    branches: list[str]
