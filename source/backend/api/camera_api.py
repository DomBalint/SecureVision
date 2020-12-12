"""
Handle the camera related REST API
"""

from flask_restful import reqparse, abort, Resource
from api.status import Status
from database.containers import Handlers

# Required headers
headers = {"Access-Control-Allow-Origin": "*"}
parser = reqparse.RequestParser()

# The objects retrieved from the databse should look something like this
camera_handler_instance = Handlers.cam_handler()

# Add exactly four cameras to the database
# mock_cameras = {
#     1: {'image_id': [1, 2, 3, 4]},
#     2: {'image_id': [1, 2, 3, 4]},
#     3: {'image_id': [1, 2, 3, 4]},
#     4: {'image_id': [1, 2, 3, 4]},
# }

# Camera id argument
parser.add_argument('camera_num')


def abort_if_there_are_no_available_cameras():
    """
    Check if there are any cameras initiated in the database
    """
    if len(camera_handler_instance.all_cams()) < 1:
        abort(Status.NOT_FOUND, message=f"There are no available cameras", headers=headers)


class CameraApi(Resource):
    """
    Handel requests related to the cameras
    """
    def get(self):
        """
        Retrieve the available cameras
        """

        abort_if_there_are_no_available_cameras()
        cameras_list = camera_handler_instance.all_cams()
        cameras_list = [{'cam_id': camera.id, 'is_running': camera.is_running} for camera in cameras_list]
        return cameras_list, Status.OK, headers

    def post(self):
        """
        Stop getting the feed from the camera
        """

        args = parser.parse_args()
        camera_num = args['camera_num']
        abort_if_there_are_no_available_cameras()
        # Check if the camera is on, then stop the feed
        success = camera_handler_instance.update_stop_camera(camera_num)
        if success:
            return {"id": camera_num}, Status.OK, headers
        # Camera is not running or it does not exist
        else:
            return None, Status.NO_CONTENT, headers
