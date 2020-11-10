import requests
from requests.auth import HTTPBasicAuth


class TestLoginApi:

    def test_login_user(self, login_data_api, api_server):
        # Setup
        desired, name, password = login_data_api
        BASE = api_server
        # Exercise
        response = requests.get(BASE + 'user/login', auth=HTTPBasicAuth(name, password))

        # Verify
        assert response.status_code == desired
        # Cleanup
