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
