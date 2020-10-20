from sqlalchemy import Column, Integer, Boolean
from sqlalchemy import Sequence

from SecureVision.source.backend.database.base import Base


class Camera(Base):
    __tablename__ = 'camera'
    id = Column(Integer, Sequence('camera_id_seq'), primary_key=True)
    is_running = Column(Boolean)

    def __repr__(self):
        return "<Camera(name='%d', is_running='%d')>" % (self.id, self.is_running)
