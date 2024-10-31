from fastapi import FastAPI

from api import router

app = FastAPI(docs_url="/", redoc_url="/redoc")
app.include_router(router)
