import requests


class TestLoginApi:

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