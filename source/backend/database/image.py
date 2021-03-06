from typing import List

from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship
from sqlalchemy.orm.query import Query

from base import Base
from unique import UniqueMixin
from unique import _unique


class Image(UniqueMixin, Base):
    __tablename__ = 'image'
    id = Column(Integer, Sequence('image_id_seq'), primary_key=True)
    img_path = Column(String(200), unique=True, nullable=False)

    cam_id = Column(Integer, ForeignKey('camera.id'), nullable=False)
    camera = relationship("Camera", backref="images")

    @classmethod
    def unique_hash(cls, img_path: str) -> str:
        """
        Returns attribute
        :param img_path: unique attribute
        :return:
        """
        return img_path

    @classmethod
    def unique_filter(cls, query: Query, img_path: str) -> Query:
        """
        Filters by unique attribute
        :param query: query object
        :param img_path: unique attribute
        :return:
        """
        return query.filter(Image.img_path == img_path)

    @classmethod
    def as_unique(cls, session, **kw):
        """
       Adds obj as unique
       :param session: session obj
       :param kw: arguments
       :return:
       """
        return _unique(
            session,
            cls,
            cls.unique_filter,
            cls,
            kw,
            'img_path'
        )

    def __repr__(self):
        return "<Image(id='%d', img_path='%s')>" % (self.id, self.img_path)


# TODO: add global session handler and not separate
class ImageHandler:

    def __init__(self, session):
        self.__session = session

    # ADD------------------------------------------------------------
    # TODO: ADD FUNCTION THAT REGISTERS IMG WITHOUT UNIQUE CHECK, FASTER
    def add_image(self, img_path: str, camera_id: int) -> None:
        """
        Adds images as unique with unique paths
        :param img_path: path to the image
        :param camera_id: id of the camera it belongs to
        """
        img = Image.as_unique(self.__session, img_path=img_path, cam_id=camera_id)
        self.__session.commit()
        return img.id

    # UPDATE------------------------------------------------------------
    def update_image_by_path(self, img_path: str, img_path_new: str, cam_id_new: int = -1) -> None:
        """
        Updates image queried by its path
        :param img_path: query argument
        :param img_path_new: new path of the image
        :param cam_id_new: new cam id if not default
        """
        img = self.img_by_path(img_path)
        if img:
            img.img_path = img_path_new
            if cam_id_new != -1:
                img.cam_id = cam_id_new
            self.commit()
        else:
            print('No such image')

    def update_image_by_id(self, img_id: int, img_path_new: str, cam_id_new: int = -1) -> None:
        """
        Updates image queried by its path
        :param img_id: query argument
        :param img_path_new: new path of the image
        :param cam_id_new: new cam id if not default
        """
        img = self.img_by_id(img_id)
        if img:
            img.img_path = img_path_new
            if cam_id_new != -1:
                img.cam_id = cam_id_new
            self.commit()
        else:
            print('No such image')

    # QUERY------------------------------------------------------------
    def img_by_path(self, im_path: str) -> Image:
        """
        Queries the images and searches by path
        :param im_path: query argument
        :return: Image object from the database that satisfies the query
        """
        return self.__session.query(Image).filter(Image.img_path == im_path).one_or_none()

    def img_by_id(self, img_id: int) -> Image:
        """
        Queries the images and searches by id
        :param img_id: query argument
        :return: Image object from the database that satisfies the query
        """
        return self.__session.query(Image).filter(Image.id == img_id).one_or_none()

    def imgs_by_cam_id(self, cam_id: int) -> List:
        """
        Queries the images and searches by cam_id
        :param cam_id: query argument, all images that belong to that specific camera
        :return: List of Image objects from the database that satisfies the query
        """
        return self.__session.query(Image).filter(Image.cam_id == cam_id).all()

    def img_last_by_cam_id(self, cam_id: int) -> Image:
        """
        Queries the images and searches by cam_id
        :param cam_id: query argument, all images that belong to that specific camera
        :return: List of Image objects from the database that satisfies the query
        """
        return self.__session.query(Image).filter(Image.cam_id == cam_id).order_by(Image.id.desc()).first()

    # DELETE------------------------------------------------------------
    def img_delete_by_path(self, img_path: str) -> None:
        """
        Deletes an image object identified by its path
        :param img_path: query argument
        """
        img = self.img_by_path(img_path)
        if img:
            self.__session.delete(img)
            self.commit()
        else:
            print('No such image')

    def img_delete_by_id(self, img_id: int) -> None:
        """
        Deletes an image object identified by its id
        :param img_id: query argument
        """
        img = self.img_by_id(img_id)
        if img:
            self.__session.delete(img)
            self.commit()
        else:
            print('No such image')

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
