from sqlalchemy.ext.declarative import declarative_base
from backend.database.base import engine

Base = declarative_base()
Base.metadata.reflect(engine)
Base.metadata.drop_all(engine)
