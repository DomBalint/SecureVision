from sqlalchemy import Column, Integer, String
from sqlalchemy import ForeignKey
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship

from SecureVision.source.backend.database.base import Base


class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, Sequence('image_id_seq'), primary_key=True)
    img_path = Column(String(200))

    cam_id = Column(Integer, ForeignKey('camera.id'))
    cam = relationship("Camera", back_populates="image")

    def __repr__(self):
        return "<Image(id='%d', img_path='%s')>" % (self.id, self.img_path)