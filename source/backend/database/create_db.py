import os

from base import Base
from containers import Handlers, Databases
from user import User
from camera import Camera
from image import Image
from annotation import Annotation
from feedback import Feedback


# Keep these imports


def create_db(num_of_cameras):
    Base.metadata.create_all(Databases.base_engine)
    # 2. Creates a session object that can be later used for adding elements and querying
    user_handler_instance = Handlers.user_handler()
    cam_handler_instance = Handlers.cam_handler()

    # As it is available only for the selected guards, random users can not register
    # During the database setup the user registration should be handled
    user_handler_instance.register_users_unique(os.path.join(os.getcwd(), 'db_json', "users.json"))

    cam_list = cam_handler_instance.all_cams()
    if len(cam_list) == num_of_cameras:
        for cam_instance in cam_list:
            cam_handler_instance.update_start_camera(cam_instance.id)
    else:
        for i in range(num_of_cameras - len(cam_list)):
            cam_handler_instance.add_camera()

        cam_new = cam_handler_instance.all_cams()
        for cam_instance in cam_new:
            cam_handler_instance.update_start_camera(cam_instance.id)

    user_handler_instance.release_resources()
    cam_handler_instance.release_resources()


if __name__ == "__main__":
    create_db(num_of_cameras=2)
