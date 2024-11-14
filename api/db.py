from fastapi_sqlalchemy import SQLAlchemy

from api.settings import settings

db = SQLAlchemy(url=settings.connection_str)
