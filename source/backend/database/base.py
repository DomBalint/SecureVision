from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event

# local sqlite database for checking things
LOCAL_URL = 'sqlite:///secure_vision.db'
DATABASE_URL = 'postgresql://vmnaxxcjwwqlkc:a20d0f30efe4cf8a8acab7d6204e6f0f2652cdaf36dc1a79a636b4f9a317fb88@ec2-54-228-209-117.eu-west-1.compute.amazonaws.com:5432/d45rfoe1nssprp'
engine = create_engine(DATABASE_URL, echo=False)

# Only for local testing, sqlite has no foreign key constraints, REMOTE DOES NOT NEED IT
# def _fk_pragma_on_connect(dbapi_con, con_record):
#     dbapi_con.execute('pragma foreign_keys=ON')

# event.listen(engine, 'connect', _fk_pragma_on_connect)

Session = sessionmaker(bind=engine)
Base = declarative_base()
