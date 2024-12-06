from fastapi import HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from api import models
from api.db import db

bearer_description = """Token authorization. Get a token by sending a POST request to `/token` endpoint (JSON-mode, preferred).
Ensure to use only those permissions that your app actually needs. `full_control` gives access to all permissions of a user
To authorize, send an `Authorization` header with value of `Bearer <token>` (replace `<token>` with your token)
"""

oauth_kwargs = {
    "tokenUrl": "/token",
    "scopes": {
        "full_control": "Full control over what current user has",
    },
}


class AuthDependency(OAuth2PasswordBearer):
    def __init__(self, token_required=True, return_token=False):
        self.return_token = return_token
        super().__init__(
            **oauth_kwargs,
            auto_error=token_required,
            scheme_name="Bearer" if token_required else "BearerOptional",
            description=bearer_description,
        )

    async def _process_request(self, request: Request, security_scopes: SecurityScopes):
        if security_scopes.scopes:
            authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
        else:
            authenticate_value = "Bearer"
        token: str = await super().__call__(request)
        exc = HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": authenticate_value},
        )
        if not token:
            raise exc
        data = await run_in_threadpool(
            db.session.query(models.User, models.Token).join(models.Token).filter(models.Token.id == token).first
        )
        if data is None:
            raise exc
        user, token = data
        forbidden_exception = HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
            headers={"WWW-Authenticate": authenticate_value},
        )
        if "full_control" not in token.scopes:
            for scope in security_scopes.scopes:
                if scope not in token.scopes:
                    raise forbidden_exception
        if self.return_token:
            return user, token
        return user

    async def __call__(self, request: Request, security_scopes: SecurityScopes):
        try:
            return await self._process_request(request, security_scopes)
        except HTTPException:
            if self.auto_error:
                raise
            if self.return_token:
                return None, None
            return None
