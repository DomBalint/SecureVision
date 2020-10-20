from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(100))
    user_pass = Column(String(50))
    user_rights = Column(Integer)
    num_feedback = Column(Integer)

    def __repr__(self):
        return "<User(name='%s', user_rights='%d')>" % (self.name, self.user_rights)


class Camera(Base):
    __tablename__ = 'camera'
    id = Column(Integer, Sequence('camera_id_seq'), primary_key=True)
    is_running = Column(Boolean)

    def __repr__(self):
        return "<Camera(name='%d', is_running='%d')>" % (self.id, self.is_running)


class Image(Base):
    __tablename__ = 'image'
    id = Column(Integer, Sequence('image_id_seq'), primary_key=True)
    img_path = Column(String(200))

    cam_id = Column(Integer, ForeignKey('camera.id'))
    cam = relationship("Camera", back_populates="camera")

    def __repr__(self):
        return "<Image(id='%d', img_path='%s')>" % (self.id, self.img_path)


class Detection(Base):
    __tablename__ = 'detection'
    id = Column(Integer, Sequence('detection_id_seq'), primary_key=True)
    img_id = Column(Integer, ForeignKey('image.id'))
    image = relationship("Image", back_populates="detection")

    def __repr__(self):
        return "<Detection(id='%d', img_id='%d')>" % (self.id, self.img_id)


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


class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, Sequence('feedback_id_seq'), primary_key=True)
    corr_obj_type = Column(String(100))
    corr_left_x = Column(Float)
    corr_left_y = Column(Float)
    corr_length = Column(Float)
    corr_width = Column(Float)
    detection_id = Column(Integer, ForeignKey('detection.id'))
    detection = relationship("Detection", back_populates="annotation")

    def __repr__(self):
        return "<Feedback(id='%s', obj_type='%s')>" % (self.id, self.corr_obj_type)
