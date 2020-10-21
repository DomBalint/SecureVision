from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Creates a local sqlite database to the database folder
# TODO: Reconsider database type, can be MySQL or MariaDB
# TODO: Migrate to remote database so it can be reached by everyone
engine = create_engine('sqlite:///secure_vision.db', echo=True)
Session = sessionmaker(bind=engine)

Base = declarative_base()
