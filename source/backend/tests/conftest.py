import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from SecureVision.source.backend.database.base import Base
from SecureVision.source.backend.database.user import User, UserHandler


def build_test_db():
    engine = create_engine('sqlite:///:memory:', echo=False)
    Base.metadata.create_all(engine)
    sessionmanager_obj = sessionmaker(bind=engine)
    user_handler_instance = UserHandler(sessionmanager_obj)
    test_session_obj = sessionmanager_obj()

    return user_handler_instance, Base, engine, test_session_obj


params_reg = [('./data_test/test_user_1.json', ['Guard1']), ('./data_test/test_user_2.json', ['Guard1', 'Guard2']),
              ('./data_test/test_user_3.json', ['Guard1', 'Guard2', 'Guard3'])]


@pytest.fixture(scope='module', params=params_reg)
def register_data(request):
    json_path, desired_output = request.param
    user_handler_instance, Base_created, engine, test_session_obj = build_test_db()
    return user_handler_instance, Base_created, engine, test_session_obj, desired_output, json_path


params_login = [('Guard1', 'Guard1'), ('Guard3', 'Guard3'),
                ('GuardNonexistent', 'None')]


@pytest.fixture(scope='module', params=params_login)
def login_data(request):
    name, desired_output = request.param
    user_handler_instance, Base_created, engine, test_session_obj = build_test_db()
    user_handler_instance.register_users('./data_test/test_user_4.json')
    return user_handler_instance, Base_created, engine, test_session_obj, desired_output, name
