from sqlalchemy.ext.declarative import declarative_base

from containers import Databases


def clean_db():
    Base = declarative_base()
    Base.metadata.reflect(Databases.base_engine)
    Base.metadata.drop_all(Databases.base_engine)


if __name__ == "__main__":
    clean_db()
