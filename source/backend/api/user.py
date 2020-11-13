"""
Handle the user related REST API
"""
from flask_restful import reqparse, abort, Resource
from source.backend.database.user import UserHandler
from source.backend.database.base import Session

headers = {"Access-Control-Allow-Origin": "*"}
parser = reqparse.RequestParser()

mock_users = {
    'Guard1': {'pass': 'pass', 'id': 1, 'name': 'Guard1', 'rights': 1},
    'Guard2': {'pass': 'pass', 'id': 2, 'name': 'Guard1', 'rights': 0},
    'Guard3': {'pass': 'pass', 'id': 3, 'name': 'Guard1', 'rights': 0},
}

# Login arguments
parser.add_argument('username')
parser.add_argument('password')


# Check the existence of the user and the correctness of the password from the database
def abort_if_username_or_password_are_incorrect(username, password):
    # user = query_user(username)
    if username not in mock_users:  # user:
        abort(401, message="Unauthorized access! username or password incorrect",
              headers=headers)
    elif mock_users[username]['pass'] != password:
        abort(401, message="Unauthorized access! username or password incorrect",
              headers=headers)
    # return user

# user_handler_instance = UserHandler(Session)


def query_user(username):
    return mock_users[username]
    # query = user_handler_instance.user_by_name(username)
    # print(query)
    # return query


def query_user_by_id(user_id):
    return mock_users[0]
    # return user_handler_instance.user_by_id(user_id)


class User(Resource):
    def get(self):
        return {'meow': "good job lil buddy"}, 200,  headers

    def post(self):
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        print(username)
        print(password)
        # user = abort_if_username_or_password_are_incorrect(username, password)
        abort_if_username_or_password_are_incorrect(username, password)
        # return the user as a json object or just the id
        return {'id': mock_users[username]['id']}, 200, headers

    # Add new user
    def put(self):
        pass

    # Remove a user
    def delete(self):
        pass

    # Update a user's information
    def update(self):
        pass
