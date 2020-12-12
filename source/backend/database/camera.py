from typing import List

from sqlalchemy import Column, Integer, Boolean
from sqlalchemy import Sequence

from database.base import Base


class Camera(Base):
    __tablename__ = 'camera'
    id = Column(Integer, Sequence('camera_id_seq'), primary_key=True)
    is_running = Column(Boolean, nullable=True)

    def __repr__(self):
        return "<Camera(name='%d', is_running='%d')>" % (self.id, self.is_running)


class CameraHandler:

    def __init__(self, session):
        self.__session = session

    # ADD------------------------------------------------------------
    def add_camera(self):
        """
        Adds camera to the db, with the default constructor
        """
        cam = Camera()
        self.__session.add(cam)
        self.__session.commit()

    # UPDATE------------------------------------------------------------
    def update_start_camera(self, cam_id: int) -> bool:
        """
        Updates, starts the camera, identified by its id
        :param cam_id: query argument
        :return if successful return true
        """
        cam = self.cam_by_id(cam_id)
        if cam:
            cam.is_running = True
            self.commit()
            return True
        else:
            print('No such camera')
            return False

    def update_stop_camera(self, cam_id: int) -> bool:
        """
        Updates, stops the camera, identified by its id
        :param cam_id: query argument
        :return if successful return true

        """
        cam = self.cam_by_id(cam_id)
        if cam:
            if cam.is_running:
                cam.is_running = False
                self.commit()
                return True
            return False
        else:
            print('No such camera')
            return False

    # QUERY------------------------------------------------------------
    def cam_by_id(self, cam_id: int) -> Camera:
        """
        Queries the cameras and searches by id
        :param cam_id: query argument
        :return: Camera object from the database that satisfies the query
        """
        return self.__session.query(Camera).filter(Camera.id == cam_id).one_or_none()

    def all_cams(self) -> List:
        """
        Queries the cameras
        :return: Camera list from the database
        """
        return self.__session.query(Camera).all()

    # DELETE------------------------------------------------------------
    def cam_delete(self, cam_id: int) -> None:
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
