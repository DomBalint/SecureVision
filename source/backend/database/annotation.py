from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import ForeignKey
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship

from SecureVision.source.backend.database.base import Base


class Annotation(Base):
    __tablename__ = 'annotation'
    id = Column(Integer, Sequence('anno_id_seq'), primary_key=True)
    obj_type = Column(String(100), nullable=False)
    left_x = Column(Float, nullable=False)
    left_y = Column(Float, nullable=False)
    length = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    detection_id = Column(Integer, ForeignKey('detection.id'), nullable=False)
    detection = relationship("Detection", backref="annotation")

    def __repr__(self):
        return "<Annotation(id='%s', obj_type='%s')>" % (self.id, self.obj_type)
