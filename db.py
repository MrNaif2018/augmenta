from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from settings import Settings

engine = create_engine(Settings.connection_str, echo=True)
Session = sessionmaker(engine)
