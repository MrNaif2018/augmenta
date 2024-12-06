from fastapi import APIRouter, Security

from api import crud, models, schemes
from api.auth import AuthDependency

router = APIRouter()


@router.post("", response_model=schemes.DisplayToken)
def create_token(data: schemes.CreateToken):
    user = crud.users.validate_user(data.email, data.password)
    token = crud.token.create({"user_id": user.id, "scopes": data.scopes})
    return token


@router.get("/me", response_model=schemes.DisplayToken)
def get_token_me(auth_data: tuple[models.User, str] = Security(AuthDependency(return_token=True))):
    return auth_data[1]
