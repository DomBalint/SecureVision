from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Creates a local sqlite database to the database folder
# TODO: Reconsider database type, can be MySQL or MariaDB
# TODO: Migrate to remote database so it can be reached by everyone
DATABASE_URL = 'postgres://hcxizfripeejzp:b8842bc09501d56dbeae98802c19f8d4fc9f51557bcf1c9f8588614c4d17f7de@ec2-54-246-115-40.eu-west-1.compute.amazonaws.com:5432/d8s5i6sv77e5kc'
engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()
