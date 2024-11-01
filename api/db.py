import typing
from contextvars import ContextVar

from fastapi_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import Session as sqla_session
from sqlalchemy.orm import sessionmaker

# from api.models import Base
from api.settings import Settings

settings = Settings()
# engine = create_engine(settings.connection_str, echo=True)
# Session = sessionmaker(engine, expire_on_commit=False)

# Base.metadata.create_all(engine)
db = SQLAlchemy(url=settings.connection_str)


# session_context_var: ContextVar[sqla_session | None] = ContextVar(
#     "_session", default=None
# )


# async def set_db() -> typing.AsyncIterator[None]:
#     """Store db session in the context var and reset it."""
#     db = Session()
#     print(db)
#     token = session_context_var.set(db)
#     print(token)
#     try:
#         yield
#     finally:
#         db.close()
#         session_context_var.reset(token)


# def get_db() -> sqla_session:
#     """Fetch db session from the context var."""
#     session = session_context_var.get()
#     if session is None:
#         msg = "Missing session"
#         raise RuntimeError(msg)
#     return session
