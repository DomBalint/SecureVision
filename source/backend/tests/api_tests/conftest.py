import os
import sys

import pytest
from xprocess import ProcessStarter


@pytest.fixture(scope='function')
def login_data_api(request):
    name, password, desired_output = request.param
    return desired_output, name, password


@pytest.fixture(scope='function')
def camera_api(request):
    cam_num, desired_output = request.param
    return desired_output, cam_num


@pytest.fixture(scope='function')
def feedback_api(request):
    feedback, camera_num, image_id, desired = request.param
    return feedback, camera_num, image_id, desired


@pytest.fixture(scope='module')
def api_server(xprocess):
    class Starter(ProcessStarter):
        # startup pattern
        pattern = "* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)"

        # command to start process
        rel_path_to_api = '...\\api\\api_class.py'
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
