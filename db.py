from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import Settings

settings = Settings()
engine = create_engine(settings.connection_str, echo=True)
Session = sessionmaker(engine)
