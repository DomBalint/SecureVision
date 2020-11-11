from sqlalchemy import Column, Integer, Boolean
from sqlalchemy import Sequence

from SecureVision.source.backend.database.base import Base


class Camera(Base):
    __tablename__ = 'camera'
    id = Column(Integer, Sequence('camera_id_seq'), primary_key=True)
    is_running = Column(Boolean, nullable=True)

    def __repr__(self):
        return "<Camera(name='%d', is_running='%d')>" % (self.id, self.is_running)


class CameraHandler:

    def __init__(self, session_maker):
        self.__session = session_maker()

    # ADD------------------------------------------------------------
    def add_camera(self):
        """
        Adds camera to the db, with the default constructor
        """
        cam = Camera()
        self.__session.add(cam)
        self.__session.commit()

    # UPDATE------------------------------------------------------------
    def update_start_camera(self, cam_id: Integer) -> None:
        """
        Updates, starts the camera, identified by its id
        :param cam_id: query argument
        """
        cam = self.cam_by_id(cam_id)
        if cam:
            cam.is_running = True
            self.commit()
        else:
            print('No such camera')

    def update_stop_camera(self, cam_id: Integer) -> None:
        """
        Updates, stops the camera, identified by its id
        :param cam_id: query argument
        """
        cam = self.cam_by_id(cam_id)
        if cam:
            cam.is_running = False
            self.commit()
        else:
            print('No such camera')

    # QUERY------------------------------------------------------------
    def cam_by_id(self, cam_id: Integer) -> Camera:
        """
        Queries the cameras and searches by id
        :param cam_id: query argument
        :return: Camera object from the database that satisfies the query
        """
        return self.__session.query(Camera).filter(Camera.id == cam_id).one_or_none()

    # DELETE------------------------------------------------------------
    def cam_delete(self, cam_id: Integer) -> None:
        """
        Deletes a camera object identified by its id
        :param cam_id: query argument
        """
        cam = self.cam_by_id(cam_id)
        if cam:
            self.__session.delete(cam)
            self.commit()
        else:
            print('No such camera')

    # RESOURCES------------------------------------------------------------
    def release_resources(self):
        """
        Releases the session object
        """
        if self.__session:
            self.__session.close()

    def commit(self):
        """
        Commits to the session
        """
        if self.__session:
            self.__session.commit()
