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


class RequestIn(Request):
    user_id: int


@router.get("/all/{user_id}", response_model=list[Request])
def get_all_requests(user_id: int):
    return requests.get_by_user_id(user_id)


@router.get("{id}", response_model=Request)
def get_request(id: int):
    request = requests.get_by_id(id)
    if request is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Request not found"
        )
    return request


@router.post("/add/{user_id}")
def add_request(user_id: int, request: Request):
    request_in = RequestIn(request)
    if requests.create(request_in):
        return JSONResponse(
            content={"message": "The request has been successfully added"},
            status_code=status.HTTP_200_OK,
        )
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@router.delete("/delete/{id}")
def delete_request(id: int):
    if not requests.delete(id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Request not found"
        )
    return JSONResponse(
        content={"message": "The request has been successfully deleted"},
        status_code=status.HTTP_200_OK,
    )
