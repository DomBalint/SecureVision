from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event


def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute('pragma foreign_keys=ON')


# local sqlite database for checking things
LOCAL_URL = 'sqlite:///secure_vision.db'
DATABASE_URL = 'postgresql://hcxizfripeejzp:b8842bc09501d56dbeae98802c19f8d4fc9f51557bcf1c9f8588614c4d17f7de@ec2-54-246-115-40.eu-west-1.compute.amazonaws.com:5432/d8s5i6sv77e5kc'
engine = create_engine(LOCAL_URL, echo=False)

event.listen(engine, 'connect', _fk_pragma_on_connect)

Session = sessionmaker(bind=engine)
Base = declarative_base()
