from sqlalchemy import Column, Integer
from sqlalchemy import ForeignKey
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship

from SecureVision.source.backend.database.base import Base


class Detection(Base):
    __tablename__ = 'detection'
    id = Column(Integer, Sequence('detection_id_seq'), primary_key=True)
    img_id = Column(Integer, ForeignKey('image.id'))
    image = relationship("Image", backref="detection")

    def __repr__(self):
        return "<Detection(id='%d', img_id='%d')>" % (self.id, self.img_id)