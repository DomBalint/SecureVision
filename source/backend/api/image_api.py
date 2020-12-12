"""
Handle the image related REST API
"""
from flask_restful import reqparse, abort, Resource
from status import Status
from containers import Handlers

headers = {"Access-Control-Allow-Origin": "*"}

parser = reqparse.RequestParser()
camera_handler_instance = Handlers.cam_handler()
img_handler_instance = Handlers.img_handler()
fb_handler_instance = Handlers.fb_handler()

# The objects retrieved from the databse should look something like this
# mock_data = {
#     1: [{'image_id': 1, "url": ""}, {'image_id': 2, "url": ""}],
#     2: [{'image_id': 1, "url": ""}, {'image_id': 2, "url": ""}],
#     3: [{'image_id': 1, "url": ""}, {'image_id': 2, "url": ""}],
#     4: [{'image_id': 1, "url": ""}, {'image_id': 2, "url": ""}],
# }

# Login arguments
parser.add_argument('camera_num')
parser.add_argument('image_id')
parser.add_argument('feedback')


def abort_if_camera_or_image_are_not_found(camera_num, image_id=None):
    """
    Check the existence of the camera num and the image id in the database
    :param camera_num: the required camera id.
    :param image_id: *optional the required image id.
    """

    cam_instance = camera_handler_instance.cam_by_id(camera_num)
    if not cam_instance:
        abort(Status.NOT_FOUND, message=f"Camera {camera_num} was not found!", headers=headers)
    if image_id is not None:
        if image_id not in [image.id for image in cam_instance.images]:
            abort(Status.NOT_FOUND, message=f"Image {image_id} was not found!", headers=headers)


class ImageApi(Resource):
    """
    Handel requests related to the Images
    """

    def post(self):
        """
        Return the last image taken by the chosen camera with it's id
        """

        args = parser.parse_args()
        camera_num = int(args['camera_num'])
        abort_if_camera_or_image_are_not_found(camera_num)
        last_image = img_handler_instance.img_last_by_cam_id(camera_num)
        last_image = {'image_id': last_image.id, 'url': last_image.img_path}
        return last_image, Status.OK, headers

    def put(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass


class FeedbackApi(Resource):
    """
        Handel requests related to the Image Feedback
    """

    def post(self):
        pass

    def put(self):
        """
        Add the a new feedback to the database
        """

        args = parser.parse_args()
        feedback = int(args['feedback'])  # convert to appropriate value
        camera_num = int(args['camera_num'])
        image_id = int(args['image_id'])
        abort_if_camera_or_image_are_not_found(camera_num, image_id)
        success = fb_handler_instance.update_create_fb_by_img_id(img_id=image_id, new_value=bool(feedback))
        if success:
            return {"success": success}, Status.OK, headers

        return {"success": success}, Status.BAD_REQUEST, headers

    def delete(self):
        pass

    def update(self):
        pass
