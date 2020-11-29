"""
Run the API and setup the routes

install Flask & flask_restful

Sample usage
curl http://localhost:5000/user/login -d "password=something&username=name" -X post -v
curl http://localhost:5000/cameras
"""
import sys
import os
sys.path.append(os.path.abspath('./'))

import datetime
from functools import wraps

import jwt
from flask import Flask, request, jsonify, make_response
from flask_restful import Api
from werkzeug.security import check_password_hash
from flask_cors import CORS
from backend.database.base import Session
from backend.database.user import UserHandler

# DEPRACATED imports
# from user import User
# from image import Image, Feedback
# from camera import Camera
# from secret import secret_key

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
api = Api(app)
app.config['CORS_ORIGINS'] = '*'
cors = CORS(app)

user_handler_instance = UserHandler(Session)


mock_users = {
    'Guard1': {'pass': 'pass', 'id': 1, 'name': 'Guard1', 'rights': 1},
    'Guard2': {'pass': 'pass', 'id': 2, 'name': 'Guard1', 'rights': 0},
    'Guard3': {'pass': 'pass', 'id': 3, 'name': 'Guard1', 'rights': 0},
}


def query_user(username):
    # return mock_users['username']
    return user_handler_instance.user_by_name(username)


def query_user_by_id(user_id):
    # return mock_users[0]
    return user_handler_instance.user_by_id(user_id)


# .......................................................#
# Custom decorators
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = query_user_by_id(data['id'])
        except:
            return jsonify({'message': 'Token is invalid!'})

        return f(current_user, *args, **kwargs)

    return decorated


# Setup REST API:
@app.route('/user/login', methods=['GET', 'POST'])
def login():
    """ API function for [login], if username/password is correct returns an authorization token. """
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response({"message": 'Could not verify'}, 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = query_user(auth.username)
    if not user:
        return make_response({"message": 'Could not verify'}, 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

    if check_password_hash(user.user_pass, auth.password):
        token = jwt.encode({'id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY'])

        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


@app.route('/user/<user_id>', methods=['PUT'])
@token_required
def promote_user(current_user, user_id):
    """ API function for promoting user to admin. """

    if not current_user.user_rights:
        return jsonify({'message': 'Cannot perform that action!'})

    else:
        return jsonify({'message': 'The user has been promoted.'})


@app.route('/image', methods=['POST'])
@token_required
def ask_for_image(current_user):
    """ API function to get [image] with a given id on a specified camera. """
    # TODO: implement this function [ask_for_image]
    return ''


@app.route('/image/feedback', methods=['PUT'])
@token_required
def give_feedback(current_user):
    # TODO: implement this function [give_feedback]
    """ API function to give feedback on image """
    return ''


@app.route('/cameras', methods=['GET'])
@token_required
def get_camera_list(current_user):
    # TODO: implement this function [get_camera_list]
    """ API function to get a list of available cameras. """
    return ''


@app.route('/cameras', methods=['POST'])
@token_required
def toggle_camera(current_user):
    # TODO: implement this function [toggle_camera]
    """ API function to start/stop camera with given id. """
    return ''


### [add_resource] method changed to [app.route] method ###
# api.add_resource(User, '/user/login')
# api.add_resource(Image, '/image')
# api.add_resource(Feedback, '/image/feedback')
# api.add_resource(Camera, '/cameras')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
