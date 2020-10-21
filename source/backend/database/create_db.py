from SecureVision.source.backend.database.base import Session, engine, Base

from SecureVision.source.backend.database.user import User
from SecureVision.source.backend.database.camera import Camera
from SecureVision.source.backend.database.image import Image
from SecureVision.source.backend.database.detection import Detection
from SecureVision.source.backend.database.annotation import Annotation
from SecureVision.source.backend.database.feedback import Feedback
# Keep these imports

Base.metadata.create_all(engine)
sessionobj = Session()
s1 = User(name='Test', user_pass="test_pass", user_rights=1, num_feedback=2)
sessionobj.add(s1)
sessionobj.commit()
