from sqlalchemy.ext.declarative import declarative_base

from containers import Databases

Base = declarative_base()
Base.metadata.reflect(Databases.base_engine)
Base.metadata.drop_all(Databases.base_engine)
