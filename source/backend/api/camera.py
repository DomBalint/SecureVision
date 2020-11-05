"""
DEPRACATED Handle the camera related REST API
"""
from flask_restful import reqparse, abort, Resource

parser = reqparse.RequestParser()

# The objects retrieved from the databse should look something like this
mock_cameras = {
    'mock_camera1': {'image_id': [1, 2, 3, 4]},
    'mock_camera2': {'image_id': [1, 2, 3, 4]},
}

# Login arguments
parser.add_argument('camera_num')


def abort_if_there_are_no_available_cameras():
    if len(mock_cameras) < 1:
        abort(404, message=f"There are no available cameras")


class Camera(Resource):

    def get(self):
        abort_if_there_are_no_available_cameras()
        return list(mock_cameras.keys())

    def post(self):
        args = parser.parse_args()
        camera_num = args['camera_num']
        abort_if_there_are_no_available_cameras()
        # stop_feed(camera_num)
        return camera_num, 201
        pass

