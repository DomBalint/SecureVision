from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import ForeignKey
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship

from SecureVision.source.backend.database.base import Base


class Annotation(Base):
    __tablename__ = 'annotation'
    id = Column(Integer, Sequence('anno_id_seq'), primary_key=True)
    obj_type = Column(String(100))
    left_x = Column(Float)
    left_y = Column(Float)
    length = Column(Float)
    width = Column(Float)
    detection_id = Column(Integer, ForeignKey('detection.id'))
    detection = relationship("Detection", back_populates="annotation")

    def __repr__(self):
        return "<Annotation(id='%s', obj_type='%s')>" % (self.id, self.obj_type)