from sqlalchemy import Column, Integer, Boolean
from sqlalchemy import Sequence

from SecureVision.source.backend.database.base import Base


class Camera(Base):
    __tablename__ = 'camera'
    id = Column(Integer, Sequence('camera_id_seq'), primary_key=True)
    is_running = Column(Boolean, nullable=False)

    def __repr__(self):
        return "<Camera(name='%d', is_running='%d')>" % (self.id, self.is_running)


class FeedbackHandler:

    def __init__(self, session_maker):
        self.__session = session_maker()

    def run_camera(self,):
        cam = Camera(is_running=True)
        self.__session.add(cam)
        self.__session.commit()

    def cam_by_id(self, cam_id):
        return self.__session.query(Camera).filter(Camera.id == cam_id).one_or_none()

    def release_resources(self):
        if self.__session:
            self.__session.close()

    def commit(self):
        if self.__session:
            self.__session.commit()