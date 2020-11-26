"""
Handle the user related REST API
"""
from flask_restful import reqparse, abort, Resource
from werkzeug.security import check_password_hash

from backend.database.containers import Handlers

headers = {"Access-Control-Allow-Origin": "*"}
parser = reqparse.RequestParser()

# Login arguments
parser.add_argument('username')
parser.add_argument('password')


# Check the existence of the user and the correctness of the password from the database
def abort_if_username_or_password_are_incorrect(username, password):
    user = query_user(username)
    if not user:  # user:
        abort(401, message="Unauthorized access! username or password incorrect",
              headers=headers)
    elif not check_password_hash(user.user_pass, password):
        abort(401, message="Unauthorized access! username or password incorrect",
              headers=headers)
    return user


user_handler_instance = Handlers.user_handler()


def query_user(username):
    user = user_handler_instance.user_by_name(username)
    return user


def query_user_by_id(user_id):
    return user_handler_instance.user_by_id(user_id)


class UserApi(Resource):
    def get(self):
        return {'ok': "good job"}, 200, headers

    def post(self):
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        user = abort_if_username_or_password_are_incorrect(username, password)
        # return the user as a json object or just the id
        return {'id': user.id}, 200, headers

    # Add new user
    def put(self):
        pass

    # Remove a user
    def delete(self):
        pass

    # Update a user's information
    def update(self):
        pass
