import requests
import pytest
from containers import Handlers


class TestLoginApi:

    @pytest.mark.parametrize('login_data_api', [('Guard10', 'pass', 401),
                                                ('Guard1', 'bad_password', 401),
                                                ('Guard1', 'Guard1pass', 200)], indirect=['login_data_api'])
    def test_login_user(self, login_data_api):
        # Setup
        desired, name, password = login_data_api
        BASE = 'http://127.0.0.1:5000/'
        # Exercise
        user = {'username': name, 'password': password}

        response = requests.post(BASE + 'user/login', data=user)

        # Verify
        assert response.status_code == desired
        # Cleanup


class TestCameraApi:

    @classmethod
    def teardown_class(cls):
        """
        Teardown any state that was previously setup with a call to
        setup_class.
        """
        cam_handler_instance = Handlers.cam_handler()
        cam_handler_instance.update_start_camera(1)
        cam_handler_instance.release_resources()
        print('Teardown class')

    @pytest.mark.parametrize('camera_api', [(1, 200),
                                            (1, 204),
                                            (2, 204),
                                            (3, 204)], indirect=['camera_api'])
    def test_post_camera(self, camera_api):
        # Setup
        desired, cam_num = camera_api
        BASE = 'http://127.0.0.1:5000/'
        # Exercise
        cam_data = {'camera_num': cam_num}
        response = requests.post(BASE + '/cameras', data=cam_data)
        # Verify
        assert response.status_code == desired
        # Cleanup


class TestFeedbackApi:

    @pytest.mark.parametrize('feedback_api', [(1, 10, 10, 404),
                                              (1, 1, 5, 404),
                                              (1, 1, 4, 200)], indirect=['feedback_api'])
    def test_post_feedback(self, feedback_api):
        # Setup
        feedback, camera_num, image_id, desired = feedback_api
        fb_data = {'feedback': feedback, 'camera_num': camera_num, 'image_id': image_id}
        BASE = 'http://127.0.0.1:5000/'
        # Exercise
        response = requests.put(BASE + '/image/feedback', data=fb_data)
        # Verify
        assert response.status_code == desired
        # Cleanup
