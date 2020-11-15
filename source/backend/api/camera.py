"""
Handle the camera related REST API
"""
from flask_restful import reqparse, abort, Resource
from source.backend.database.camera import CameraHandler
from source.backend.database.base import Session

# Required headers
headers = {"Access-Control-Allow-Origin": "*"}
parser = reqparse.RequestParser()

# The objects retrieved from the databse should look something like this
camera_handler_instance = CameraHandler(Session)
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
    if len(camera_handler_instance.all_cams()) < 1:
        abort(404, message=f"There are no available cameras", headers=headers)


class Camera(Resource):

    def get(self):
        abort_if_there_are_no_available_cameras()
        cameras_list = camera_handler_instance.all_cams()
        cameras_list = [{'cam_id': camera.id, 'is_running': camera.is_running} for camera in cameras_list]
        return cameras_list, 200, headers

    def post(self):
        args = parser.parse_args()
        camera_num = args['camera_num']
        abort_if_there_are_no_available_cameras()
        success = camera_handler_instance.update_stop_camera(camera_num)  # check if the camera is on then stop the feed
        if success:
            return {"id": camera_num}, 200, headers
        # Camera is not running or it does not exist
        else:
            return {"id": camera_num}, 400, headers
