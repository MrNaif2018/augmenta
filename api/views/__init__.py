from fastapi import APIRouter

from api.views.lookup import router as lookup_router
from api.views.requests import router as request_router
from api.views.users import router as user_router

router = APIRouter()

router.include_router(user_router, prefix="/users")
router.include_router(request_router, prefix="/requests")
router.include_router(lookup_router, prefix="/lookup")
