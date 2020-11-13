"""
Handle the image related REST API
"""
from flask_restful import reqparse, abort, Resource

headers = {"Access-Control-Allow-Origin": "*"}
parser = reqparse.RequestParser()

# The objects retrieved from the databse should look something like this
mock_data = {
    1: [{'image_id': 1, "url": ""}, {'image_id': 2, "url": ""}],
    2: [{'image_id': 1, "url": ""}, {'image_id': 2, "url": ""}],
    3: [{'image_id': 1, "url": ""}, {'image_id': 2, "url": ""}],
    4: [{'image_id': 1, "url": ""}, {'image_id': 2, "url": ""}],
}

# Login arguments
parser.add_argument('camera_num')
parser.add_argument('image_id')
parser.add_argument('feedback')


# Check the existence of the camera num and the image id in the database
def abort_if_camera_or_image_are_not_found(camera_num, image_id=None):
    if camera_num not in list(mock_data.keys()):
        abort(404, message=f"Camera {camera_num} was not found!", headers=headers)
    if image_id is not None:
        if image_id not in [i['image_id'] for i in mock_data[camera_num]]:
            abort(404, message=f"Image {image_id} was not found!", headers=headers)


class Image(Resource):

    # Return the last image taken by the chosen camera with it's id
    def post(self):
        args = parser.parse_args()
        camera_num = int(args['camera_num'])
        abort_if_camera_or_image_are_not_found(camera_num)
        # last_image = get_last_image_from_db()
        return mock_data[camera_num][-1], 200, headers

    def put(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass


class Feedback(Resource):
    def post(self):
       pass

    # return true if the feedback was posted successfully
    def put(self):
        args = parser.parse_args()
        feedback = args['feedback']  # convert to appropriate value
        camera_num = int(args['camera_num'])
        image_id = int(args['image_id'])
        abort_if_camera_or_image_are_not_found(camera_num, image_id)
        # success = add_feedback(camera_num, image_id, feedback)
        success = True
        if success:
            return {"success": success}, 201, headers

        return {"success": success}, 400, headers

    def delete(self):
        pass

    def update(self):
        pass
