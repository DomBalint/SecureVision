import sys
import os

sys.path.append(os.path.abspath('./'))

from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from api.camera_api import CameraApi
from api.image_api import ImageApi, FeedbackApi
from api.user_api import UserApi

"""
Run the API and setup the routes

install Flask & flask_restful

Sample usage
curl http://localhost:5000/user/login -d "password=something&username=name" -X post -v
curl http://localhost:5000/cameras
"""

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
api = Api(app)
app.config['CORS_ORIGINS'] = '*'
cors = CORS(app)

api.add_resource(UserApi, '/user/login')
api.add_resource(ImageApi, '/image')
api.add_resource(FeedbackApi, '/image/feedback')
api.add_resource(CameraApi, '/cameras')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(port=port, debug=False)
