from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware

from api.db import db
from api.views import router


def get_app():
    app = FastAPI(docs_url="/", redoc_url="/redoc")
    app.include_router(router)
    app.add_middleware(DBSessionMiddleware, db=db)

    return app


app = get_app()
