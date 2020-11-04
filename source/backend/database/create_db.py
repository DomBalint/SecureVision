from SecureVision.source.backend.database.base import Session, engine, Base

from SecureVision.source.backend.database.user import User
from SecureVision.source.backend.database.camera import Camera
from SecureVision.source.backend.database.image import Image
from SecureVision.source.backend.database.detection import Detection
from SecureVision.source.backend.database.annotation import Annotation
from SecureVision.source.backend.database.feedback import Feedback
# Keep these imports

# 0. Remove it if you don't want to drop the tables
Base.metadata.drop_all(engine)
# 1. Creates the tables based on the defined classes
Base.metadata.create_all(engine)
# 2. Creates a session object that can be later used for adding elements and querying
session_obj = Session()
# 3. Creates a Test user 1
u1 = User.as_unique(session_obj, name='Test1', user_pass='test_pass', user_rights=1, num_feedback=5)
# 4. Creates a Test user 2 with the same name
u2 = User.as_unique(session_obj, name='Test1', user_pass='test_pass', user_rights=1, num_feedback=5)
# 5. No need for session_obj.add, the function already adds them
# 6. You will NOT get an UNIQUE error message for the user name
session_obj.commit()
session_obj.close()
