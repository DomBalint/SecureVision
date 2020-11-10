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
    image_id = Column(Integer, ForeignKey('image.id'), nullable=False)
    image = relationship("Image", backref="annotation")

    def __repr__(self):
        return "<Annotation(id='%s', obj_type='%s')>" % (self.id, self.obj_type)


class AnnotationHandler:

    def __init__(self, session_maker):
        self.__session = session_maker()

    # For an example see the annotations.json
    def add_annotation(self, data_dict):
        for annotation in data_dict['Annotations']:
            annotation_obj = Annotation(obj_type=annotation['obj_type'], left_x=annotation['left_x'],
                                        left_y=annotation['left_y'], length=annotation['length'],
                                        width=annotation['width'],
                                        image_id=annotation['image_id'])
            self.__session.add(annotation_obj)
        self.__session.commit()

    def anns_by_img_id(self, img_id):
        return self.__session.query(Annotation).filter(Annotation.image_id == img_id).all()

    def release_resources(self):
        if self.__session:
            self.__session.close()

    def commit(self):
        if self.__session:
            self.__session.commit()
