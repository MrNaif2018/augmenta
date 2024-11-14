from fastapi import APIRouter

from api import crud, schemes

router = APIRouter()


@router.get("", response_model=list[schemes.DisplayRequest])
def get_all_requests():
    return crud.request.get_all()


@router.get("/{model_id}", response_model=schemes.DisplayRequest)
def get_request(model_id: str):
    return crud.request.get_by_id(model_id)


@router.delete("/{model_id}")
def delete_request(model_id: str):
    return crud.request.delete(model_id)
