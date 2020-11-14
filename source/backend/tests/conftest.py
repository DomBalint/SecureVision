import os

import pytest
from xprocess import ProcessStarter
import sys
import os
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


params_login = [('Guard1', 'Guard1', 'Guard1pass'), ('Guard3', 'Guard3', 'Guard3pass'), ('GuardNone', 'None', 'None')]


@pytest.fixture(scope='module', params=params_login)
def login_data(request):
    name, desired_output, desired_pass = request.param
    user_handler_instance, Base_created, engine, test_session_obj = build_test_db()
    user_handler_instance.register_users_unique('./data_test/test_user_4.json')
    return user_handler_instance, Base_created, engine, test_session_obj, desired_output, name, desired_pass


params_fb = [('Guard1', 1)]


@pytest.fixture(scope='module', params=params_fb)
def fb_data(request):
    name, desired_output = request.param
    user_handler_instance, Base_created, engine, test_session_obj = build_test_db()
    user_handler_instance.register_users_unique('./data_test/test_user_4.json')
    return user_handler_instance, Base_created, engine, test_session_obj, desired_output, name


params_login_api = [('Guard10', 'pass', 401), ('Guard1', 'bad_password', 401), ('Guard1', 'Guard1pass', 200)]


@pytest.fixture(scope='module', params=params_login_api)
def login_data_api(request):
    name, password, desired_output = request.param
    return desired_output, name, password


@pytest.fixture(scope='module')
def api_server(xprocess):
    class Starter(ProcessStarter):
        # startup pattern
        pattern = "* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)"

        # command to start process
        rel_path_to_api = '..\\api\\api_class.py'
        path_to_api = os.path.join(os.path.abspath(sys.path[0]), rel_path_to_api)

        args = ['py', path_to_api]

        # max startup waiting time
        # optional, defaults to 120 seconds
        timeout = 45

        # max lines read from stdout when matching pattern
        # optional, defaults to 100 lines
        max_read_lines = 1000

    # db_status = test_db()
    # ensure process is running and return its logfile
    logfile = xprocess.ensure("api_server", Starter)

    conn = 'http://127.0.0.1:5000/'  # create a connection or url/port info to the server
    yield conn

    # clean up whole process tree afterwards
    xprocess.getinfo("api_server").terminate()
