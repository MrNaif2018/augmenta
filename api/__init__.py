from fastapi import APIRouter

from api.requests import router as request_router
from api.users import router as user_router

router = APIRouter()

router.include_router(user_router, prefix="/users")
router.include_router(request_router, prefix="/requests")
