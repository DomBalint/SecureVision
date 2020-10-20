from SecureVision.source.backend.database.user import User
from SecureVision.source.backend.database.camera import Camera
from SecureVision.source.backend.database.image import Image
from SecureVision.source.backend.database.detection import Detection
from SecureVision.source.backend.database.annotation import Annotation
from SecureVision.source.backend.database.feedback import Feedback

from SecureVision.source.backend.database.base import Session, engine, Base


Base.metadata.create_all(engine)
