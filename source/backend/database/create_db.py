import os

from SecureVision.source.backend.database.base import Session, engine, Base
from SecureVision.source.backend.database.user import User, UserHandler
from SecureVision.source.backend.database.camera import Camera
from SecureVision.source.backend.database.image import Image
from SecureVision.source.backend.database.annotation import Annotation
from SecureVision.source.backend.database.feedback import Feedback
# Keep these imports

# 1. Creates the tables based on the defined classes
Base.metadata.create_all(engine)
# 2. Creates a session object that can be later used for adding elements and querying
user_handler_instance = UserHandler(Session)
# As it is available only for the selected guards, random users can not register
# During the database setup the user registration should be handled
user_handler_instance.register_users_unique(os.path.join(os.getcwd(), 'db_json', "users.json"))
user_handler_instance.release_resources()

# ORDER OF ADDING THINGS: USERS, CAMERAS, IMAGES, ANNOTATIONS, FEEDBACKS
