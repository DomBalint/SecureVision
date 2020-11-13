"""
Run the API and setup the routes

install Flask & flask_restful

Sample usage
curl http://localhost:5000/user/login -d "password=something&username=name" -X post -v
curl http://localhost:5000/cameras
"""

import datetime
from functools import wraps

import jwt
from flask import Flask, request, jsonify, make_response
from flask_restful import Api
from werkzeug.security import check_password_hash
from flask_cors import CORS
from source.backend.database.base import Session
from source.backend.database.user import UserHandler

# DEPRACATED imports
from source.backend.api.user import User
from source.backend.api.image import Image, Feedback
from source.backend.api.camera import Camera

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
api = Api(app)
app.config['CORS_ORIGINS'] = '*'
cors = CORS(app)

api.add_resource(User, '/user/login')
api.add_resource(Image, '/image')
api.add_resource(Feedback, '/image/feedback')
api.add_resource(Camera, '/cameras')


if __name__ == '__main__':
    app.run(port=5000, debug=True)
