import os

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from SecureVision.source.backend.database.base import Base
from SecureVision.source.backend.database.user import User, UserHandler
from unittest import mock
from werkzeug.security import generate_password_hash

def build_test_db():
    engine = create_engine('sqlite:///:memory:', echo=False)
    Base.metadata.create_all(engine)
    sessionmanager_obj = sessionmaker(bind=engine)
    user_handler_instance = UserHandler(sessionmanager_obj)
    test_session_obj = sessionmanager_obj()

    return user_handler_instance, Base, engine, test_session_obj


params_reg = [('test_user_1.json', ['Guard1']), ('test_user_2.json', ['Guard1', 'Guard2']),
              ('test_user_3.json', ['Guard1', 'Guard2', 'Guard3'])]


@pytest.fixture(scope='module', params=params_reg)
def register_data(request):
    json_path, desired_output = request.param
    json_path = os.path.join(os.getcwd(), 'data_test', json_path)
    user_handler_instance, Base_created, engine, test_session_obj = build_test_db()
    return user_handler_instance, Base_created, engine, test_session_obj, desired_output, json_path


params_login = [('Guard1', 'Guard1'), ('Guard3', 'Guard3'),
                ('GuardNonexistent', 'None')]


@pytest.fixture(scope='module', params=params_login)
def login_data(request):
    name, desired_output = request.param
    user_handler_instance, Base_created, engine, test_session_obj = build_test_db()
    user_handler_instance.register_users_unique('./data_test/test_user_4.json')
    return user_handler_instance, Base_created, engine, test_session_obj, desired_output, name

# PART FOR THE API TESTS
# TODO MOCK DB CONNECTION AND MOCK API AND SERVER CONNECTION

params_login_api = [('Guard10', 'pass', 401), ('Guard1', 'bad_password', 401), ('Guard1', 'Guard1pass', 200)]


@pytest.fixture(scope='module', params=params_login_api)
def login_data_api(request):
    name, password, desired_output = request.param
    return desired_output, name, password
