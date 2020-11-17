import os

from SecureVision.source.backend.database.base import Base
from containers import Handlers, Databases
from SecureVision.source.backend.database.user import User
from SecureVision.source.backend.database.camera import Camera
from SecureVision.source.backend.database.image import Image
from SecureVision.source.backend.database.annotation import Annotation
from SecureVision.source.backend.database.feedback import Feedback
# Keep these imports


if __name__ == "__main__":

    # 1. Creates the tables based on the defined classes
    Base.metadata.create_all(Databases.base_engine)
    # 2. Creates a session object that can be later used for adding elements and querying
    user_handler_instance = Handlers.user_handler()

    # As it is available only for the selected guards, random users can not register
    # During the database setup the user registration should be handled
    user_handler_instance.register_users_unique(os.path.join(os.getcwd(), 'db_json', "users.json"))
    user_handler_instance.commit()
    user_handler_instance.release_resources()
    # cam_handler_instance.add_camera()
    # cam_handler_instance.add_camera()
    # for i in range(1, 5):
    #     img_handler_instance.add_image(img_path=f'Path{i}', camera_id=1)
    #
    # for i in range(6, 10):
    #     img_handler_instance.add_image(img_path=f'Path{i}', camera_id=2)
    #
    # test_cam = cam_handler_instance.cam_by_id(1)
    # for elem in test_cam.images:
    #     print(elem)
    print("DB created.")
    # ORDER OF ADDING THINGS: USERS, CAMERAS, IMAGES, ANNOTATIONS, FEEDBACKS
