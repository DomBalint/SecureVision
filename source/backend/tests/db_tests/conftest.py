import os

import pytest
from sqlalchemy import create_engine
from SecureVision.source.backend.database.user import User, UserHandler
from SecureVision.source.backend.database.camera import Camera, CameraHandler
from SecureVision.source.backend.database.image import Image, ImageHandler
from SecureVision.source.backend.database.annotation import Annotation, AnnotationHandler
from SecureVision.source.backend.database.feedback import Feedback, FeedbackHandler
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker

from SecureVision.source.backend.database.base import Base


def _fk_pragma_on_connect(dbapi_con, con_record):
    dbapi_con.execute('pragma foreign_keys=ON')


def build_db(instance):
    engine = create_engine('sqlite:///:memory:', echo=False)
    event.listen(engine, 'connect', _fk_pragma_on_connect)
    Base.metadata.create_all(engine)
    sessionmanager_obj = sessionmaker(bind=engine)
    handler_instance = []
    for inst in instance:
        if inst == 'user':
            handler_instance.append(UserHandler(sessionmanager_obj()))
        elif inst == 'cam':
            handler_instance.append(CameraHandler(sessionmanager_obj()))
        elif inst == 'img':
            handler_instance.append(ImageHandler(sessionmanager_obj()))
        elif inst == 'ann':
            handler_instance.append(AnnotationHandler(sessionmanager_obj()))
        elif inst == 'fb':
            handler_instance.append(FeedbackHandler(sessionmanager_obj()))
    test_session_obj = sessionmanager_obj()

    return handler_instance, Base, engine, test_session_obj


# DB TEST CLASS USER
params_reg = [('test_user_1.json', ['Guard1']), ('test_user_2.json', ['Guard1', 'Guard2']),
              ('test_user_3.json', ['Guard1', 'Guard2', 'Guard3'])]


@pytest.fixture(scope='module', params=params_reg)
def register_data(request):
    json_path, desired_output = request.param
    json_path = os.path.join(os.getcwd(), 'data_test', json_path)
    user_handler_instance, Base_created, engine, test_session_obj = build_db(['user'])
    return user_handler_instance[0], Base_created, engine, test_session_obj, desired_output, json_path


@pytest.fixture(scope='function')
def user_data(request):
    desired, name, pass_desired = request.param
    user_handler_instance, Base_created, engine, test_session_obj = build_db(['user'])
    user_handler_instance[0].register_users_unique('./data_test/test_user_4.json')
    return user_handler_instance[0], Base_created, engine, test_session_obj, name, desired, pass_desired


# DB TEST CLASS CAM
@pytest.fixture(scope='function')
def cam_all(request):
    desired_output = request.param
    cam_handler_instance, Base_created, engine, test_session_obj = build_db(['cam'])
    return cam_handler_instance[0], Base_created, engine, test_session_obj, desired_output


@pytest.fixture(scope='function')
def img_all(request):
    desired_output = request.param
    handler_instance, Base_created, engine, test_session_obj = build_db(['img', 'cam'])
    return handler_instance[0], handler_instance[1], Base_created, engine, test_session_obj, desired_output


@pytest.fixture(scope='function')
def fb_all(request):
    desired_output = request.param
    handler_instance, Base_created, engine, test_session_obj = build_db(['img', 'fb', 'cam'])
    return handler_instance[0], handler_instance[1], handler_instance[2], \
           Base_created, engine, test_session_obj, desired_output


@pytest.fixture(scope='function')
def ann_all(request):
    desired_output = request.param
    handler_instance, Base_created, engine, test_session_obj = build_db(['img', 'cam', 'ann'])
    return handler_instance[0], handler_instance[1], handler_instance[
        2], Base_created, engine, test_session_obj, desired_output
