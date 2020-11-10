from sqlalchemy import Column, Integer, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship

from SecureVision.source.backend.database.base import Base


class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, Sequence('feedback_id_seq'), primary_key=True)
    correct_detection = Column(Boolean, nullable=True)
    image_id = Column(Integer, ForeignKey('image.id'), nullable=False)
    image = relationship("Image", backref="feedback", uselist=False)

    def __repr__(self):
        return "<Feedback(id='%s', obj_type='%s')>" % (self.id, self.correct_detection)


class FeedbackHandler:

    def __init__(self, session_maker):
        self.__session = session_maker()

    def add_fb(self, det_correct, img_id):
        fb = Feedback(correct_detection=det_correct, image_id=img_id)
        self.__session.add(fb)
        self.__session.commit()

    def fb_by_det_id(self, det_id):
        return self.__session.query(Feedback).filter(Feedback.image_id == det_id).one_or_none()

    def fb_by_id(self, fb_id):
        return self.__session.query(Feedback).filter(Feedback.id == fb_id).one_or_none()

    def release_resources(self):
        if self.__session:
            self.__session.close()

    def commit(self):
        if self.__session:
            self.__session.commit()
