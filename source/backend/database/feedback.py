from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import ForeignKey
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship

from SecureVision.source.backend.database.base import Base


class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, Sequence('feedback_id_seq'), primary_key=True)
    corr_obj_type = Column(String(100), nullable=True)
    corr_left_x = Column(Float, nullable=True)
    corr_left_y = Column(Float, nullable=True)
    corr_length = Column(Float, nullable=True)
    corr_width = Column(Float, nullable=True)
    detection_id = Column(Integer, ForeignKey('detection.id'), nullable=False)
    detection = relationship("Detection", backref="feedback")

    def __repr__(self):
        return "<Feedback(id='%s', obj_type='%s')>" % (self.id, self.corr_obj_type)
