"""
DEPRACATED Handle the image related REST API
"""
from flask_restful import reqparse, abort, Resource

parser = reqparse.RequestParser()

# The objects retrieved from the databse should look something like this
mock_cameras = {
    'mock_camera1': {'image_id': [1, 2, 3, 4]},
}

# Login arguments
parser.add_argument('camera_num')
parser.add_argument('image_id')
parser.add_argument('feedback')


# Check the existence of the camera num and the image id in the database
def abort_if_camera_or_image_are_not_found(camera_num, image_id):
    if camera_num not in mock_cameras:
        abort(404, message=f"Camera {camera_num} was not found!")
    elif int(image_id) not in mock_cameras[camera_num]['image_id']:
        abort(404, message=f"Image {image_id} was not found!")


class Image(Resource):
    def post(self):
        args = parser.parse_args()
        camera_num = args['camera_num']
        image_id = args['image_id']
        abort_if_camera_or_image_are_not_found(camera_num, image_id)
        return camera_num, 200

    def put(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass


class Feedback(Resource):
    def post(self):
       pass

    def put(self):
        args = parser.parse_args()
        feedback = args['feedback']
        # add_feedback(camera_num, image_id, feedback)
        return feedback, 201

    def delete(self):
        pass

    def update(self):
        pass
