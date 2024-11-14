from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.middleware.cors import CORSMiddleware

from api.db import db
from api.views import router


def get_app():
    app = FastAPI(docs_url="/", redoc_url="/redoc")
    app.include_router(router)
    app.add_middleware(DBSessionMiddleware, db=db)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["Content-Disposition"],
    )

    return app


app = get_app()
