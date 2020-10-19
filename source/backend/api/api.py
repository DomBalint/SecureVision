"""
Run the API and setup the routes

install Flask & flask_restful

Sample usage
curl http://localhost:5000/user/login -d "password=something&username=name" -X post -v
curl http://localhost:5000/cameras
"""

from flask import Flask
from flask_restful import Api
from user import User
from image import Image, Feedback
from camera import Camera

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
api = Api(app)

# setup the routes
api.add_resource(User, '/user/login')
api.add_resource(Image, '/image')
api.add_resource(Feedback, '/image/feedback')
api.add_resource(Camera, '/cameras')


if __name__ == '__main__':
    app.run(debug=True)
