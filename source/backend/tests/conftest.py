import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from SecureVision.source.backend.database.base import Base
from SecureVision.source.backend.database.user import User


def build_test_db():
    engine = create_engine('sqlite:///:memory:', echo=False)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session_obj = Session()

    return session_obj, Base, engine


params = [('./data_test/test_user_1.json', ['Guard1']), ('./data_test/test_user_2.json', ['Guard1', 'Guard2']),
          ('./data_test/test_user_3.json', ['Guard1', 'Guard2', 'Guard3'])]


@pytest.fixture(scope='module', params=params)
def register_data(request):
    json_path, desired_output = request.param
    session_obj, Base_created, engine = build_test_db()
    return session_obj, Base_created, engine, desired_output, json_path
