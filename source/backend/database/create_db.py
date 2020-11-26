import os

from backend.database.base import Base
from containers import Handlers, Databases
from backend.database.user import User
from backend.database.camera import Camera
from backend.database.image import Image
from backend.database.annotation import Annotation
from backend.database.feedback import Feedback
# Keep these imports


if __name__ == "__main__":

    # 1. Creates the tables based on the defined classes
    Base.metadata.create_all(Databases.base_engine)
    # 2. Creates a session object that can be later used for adding elements and querying
    user_handler_instance = Handlers.user_handler()
    cam_handler_instance = Handlers.cam_handler()
    img_handler_instance = Handlers.img_handler()

    # As it is available only for the selected guards, random users can not register
    # During the database setup the user registration should be handled
    user_handler_instance.register_users_unique(os.path.join(os.getcwd(), 'db_json', "users.json"))
    cam_handler_instance.add_camera()
    cam_handler_instance.add_camera()
    cam_handler_instance.update_start_camera(1)
    for i in range(1, 5):
        img_handler_instance.add_image(img_path=f'Path{i}', camera_id=1)

    for i in range(6, 10):
        img_handler_instance.add_image(img_path=f'Path{i}', camera_id=2)

    user_handler_instance.release_resources()
    cam_handler_instance.release_resources()
    img_handler_instance.release_resources()
    print('DB WAS CREATED')
    # ORDER OF ADDING THINGS: USERS, CAMERAS, IMAGES, ANNOTATIONS, FEEDBACKS
