"""
DEPRACATED Handle the user related REST API
"""
from flask_restful import reqparse, abort, Resource
# import jwt
# import datetime


parser = reqparse.RequestParser()


mock_users = {
    'mock_user1': {'password': 'password', 'id': 6546543},
    'mock_user2': {'password': 'password', 'id': 1325832},
    'mock_user3': {'password': 'password', 'id': 6666666},
}

# Login arguments
parser.add_argument('username')
parser.add_argument('password')


# Check the existence of the user and the correctness of the password from the database
def abort_if_username_or_password_are_incorrect(username, password):
    if username not in mock_users:
        abort(401, message="Unauthorized access! username or password incorrect")
    elif mock_users[username]['password'] != password:
        abort(401, message="Unauthorized access! username or password incorrect")



class User(Resource):
    def post(self):
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        # abort_if_username_or_password_are_incorrect(username, password)
        # token = jwt.encode({'id' : mock_users[username]['id'], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, secret_key)
        # return {'token' : token.decode('UTF-8')}, 200
        return {'username': username}, 200

    def put(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass
