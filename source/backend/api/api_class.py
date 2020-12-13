import sys
import os

sys.path.append(os.path.abspath('./'))

from flask import Flask
from flask_cors import CORS
from flask_restful import Api

from camera_api import CameraApi
from image_api import ImageApi, FeedbackApi
from user_api import UserApi
from svlib.svtools import svtools as svt

"""
Run the API and setup the routes

install Flask & flask_restful

Sample usage
curl http://localhost:5000/user/login -d "password=something&username=name" -X post -v
curl http://localhost:5000/cameras
"""

app = Flask(
    __name__,
    template_folder=os.path.join(os.getcwd(),"frontend"),
    static_url_path="",
    static_folder=os.path.join(os.getcwd(), "frontend", "assets")
)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
api = Api(app)
app.config['CORS_ORIGINS'] = '*'
cors = CORS(app)

api.add_resource(UserApi, '/user/login')
api.add_resource(ImageApi, '/image')
api.add_resource(FeedbackApi, '/image/feedback')
api.add_resource(CameraApi, '/cameras')

if __name__ == '__main__':
    
    port = svt.conf.get('api', 'port')
    app.run(host='0.0.0.0', port=port, debug=True)
