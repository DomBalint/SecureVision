"""
Handle the camera related REST API
"""
from flask_restful import reqparse, abort, Resource
# Required headers
headers = {"Access-Control-Allow-Origin": "*"}
parser = reqparse.RequestParser()

# The objects retrieved from the databse should look something like this
# Add exactly four cameras to the database
mock_cameras = {
    1: {'image_id': [1, 2, 3, 4]},
    2: {'image_id': [1, 2, 3, 4]},
    3: {'image_id': [1, 2, 3, 4]},
    4: {'image_id': [1, 2, 3, 4]},
}

# Camera id argument
parser.add_argument('camera_num')


def abort_if_there_are_no_available_cameras():
    if len(mock_cameras) < 1:
        abort(404, message=f"There are no available cameras", headers=headers)


class Camera(Resource):

    def get(self):
        abort_if_there_are_no_available_cameras()
        # cameras_list = get_cameras_from_db()
        return list(mock_cameras.keys()), 200, headers

    def post(self):
        args = parser.parse_args()
        camera_num = args['camera_num']
        abort_if_there_are_no_available_cameras()
        # success  = stop_feed(camera_num) # check if the camera is playing then stop the feed
        success = True
        if success:
            return {"id": camera_num}, 200, headers
        else:
            return {"id": camera_num}, 400, headers

