import requests
from requests.auth import HTTPBasicAuth

# BASE = 'http://127.0.0.1:5000/'


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

# Try login: bad username
# response = requests.get(BASE + 'user/login', auth=HTTPBasicAuth('Guard10', 'pass'))
# print("401 expected:")
# print(response)
# print('')

# # Try login: bad password
# response = requests.get(BASE + 'user/login', auth=HTTPBasicAuth('Guard1', 'bad_password'))
# print("401 expected:")
# print(response)
# print('')
#
# # Try login:  good username and password (with admin)
# response = requests.get(BASE + 'user/login', auth=HTTPBasicAuth('Guard1', 'Guard1pass'))
# mock1_token = response.json()['token']
# print('Valid token expected:')
# print(response.json())
# print('')

# # Try login:  good username and password (without admin)
# response = requests.get(BASE + 'user/login', auth=HTTPBasicAuth('Guard3', 'Guard3pass'))
# mock2_token = response.json()['token']
# print('Valid token expected:')
# print(response.json())
# print('')
#
# # Try admin function: with NOT an admin user
# header = {'x-access-token': mock2_token}
# response = requests.put(BASE + 'user/6666666', headers=header)
# print('Cannot perform expected:')
# print(response.json())
# print('')

# Try admin function: with an admin user
# header = {'x-access-token': mock1_token}
# response = requests.put(BASE + 'user/6666666', headers=header)
# print('Success expected:')
# print(response.json())
# print('')
#
# # Try function (auth token required): NO auth token given
# response = requests.put(BASE + 'cameras')
# print("405 expected:")
# print(response)
# print('')
#
# # Try function (auth token required): auth token given
# header = {'x-access-token': mock1_token}
# response = requests.get(BASE + 'cameras', headers=header)
# print("200 expected:")
# print(response)
# print('')
