from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship

from SecureVision.source.backend.database.base import Base
from SecureVision.source.backend.database.unique import UniqueMixin
from SecureVision.source.backend.database.unique import _unique


class Image(UniqueMixin, Base):
    __tablename__ = 'image'
    id = Column(Integer, Sequence('image_id_seq'), primary_key=True)
    img_path = Column(String(200), unique=True, nullable=False)

    cam_id = Column(Integer, ForeignKey('camera.id'), nullable=False)
    camera = relationship("Camera", backref="images")

    @classmethod
    def unique_filter(cls, query, img_path):
        return query.filter(Image.img_path == img_path)

    @classmethod
    def as_unique(cls, session, **kw):
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

    def __init__(self, session_maker):
        self.__session = session_maker()

    # TODO: ADD FUNCTION THAT REGISTERS IMG WITHOUT UNIQUE CHECK, FASTER
    def add_image(self, img_path, camera_id):
        Image.as_unique(self.__session, img_path=img_path, cam_id=camera_id)
        self.__session.commit()

    def img_by_path(self, im_path):
        return self.__session.query(Image).filter(Image.img_path == im_path).one_or_none()

    def img_by_id(self, img_id):
        return self.__session.query(Image).filter(Image.id == img_id).one_or_none()

    def release_resources(self):
        if self.__session:
            self.__session.close()

    def commit(self):
        if self.__session:
            self.__session.commit()
