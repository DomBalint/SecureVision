import json
from typing import List, Dict

from sqlalchemy import Column, Integer, String, Float
from sqlalchemy import ForeignKey
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship

from SecureVision.source.backend.database.base import Base


class Annotation(Base):
    __tablename__ = 'annotation'
    id = Column(Integer, Sequence('anno_id_seq'), primary_key=True)
    obj_type = Column(String(100), nullable=False)
    obj_confidence = Column(Float, nullable=False)
    left_x = Column(Float, nullable=False)
    left_y = Column(Float, nullable=False)
    length = Column(Float, nullable=False)
    width = Column(Float, nullable=False)
    image_id = Column(Integer, ForeignKey('image.id'), nullable=False)
    image = relationship("Image", backref="annotation")

    def __repr__(self):
        return "<Annotation(id='%s', obj_type='%s')>" % (self.id, self.obj_type)


class AnnotationHandler:

    def __init__(self, session):
        self.__session = session

    # ADD------------------------------------------------------------
    def add_annotations_from_dict(self, annotation_dict: Dict) -> None:
        """
        Adds the annotations the db, from a given dictionary. For an example see the annotations.json
        :param annotation_dict: a dictionary which contains the annotations
        """
        for annotation in annotation_dict['Annotations']:
            annotation_obj = Annotation(obj_type=annotation['obj_type'],
                                        obj_confidence=annotation['obj_confidence'],
                                        left_x=annotation['left_x'],
                                        left_y=annotation['left_y'],
                                        length=annotation['length'],
                                        width=annotation['width'],
                                        image_id=annotation['image_id'])
            self.__session.add(annotation_obj)
        self.commit()

    def add_annotations_from_path(self, json_file_path: str) -> None:
        """
        Adds the annotations the db, from a given dictionary. For an example see the annotations.json
        :param json_file_path: path to the json file
        """
        with open(json_file_path, 'r') as file:
            annotation_dict = json.load(file)
            for annotation in annotation_dict['Annotations']:
                annotation_obj = Annotation(obj_type=annotation['obj_type'],
                                            obj_confidence=annotation['obj_confidence'],
                                            left_x=annotation['left_x'],
                                            left_y=annotation['left_y'],
                                            length=annotation['length'],
                                            width=annotation['width'],
                                            image_id=annotation['image_id'])
                self.__session.add(annotation_obj)
        self.commit()

    # UPDATE------------------------------------------------------------
    def update_anns_by_img_id(self, img_id: int, annotation_dict_new: Dict) -> None:
        """
        Query and update all the annotations to a specific image, the new values are from the new ann dict.
        Not the best solution but in this case there can be multiple things that need to be updated. So first delete
        all the old ones and add everything as new.
        :param img_id: id of the specific image
        :param annotation_dict_new: new annotation dict
        """
        # TODO: Find better solution
        self.anns_delete_by_img_id(img_id)
        self.add_annotations_from_dict(annotation_dict_new)

    # QUERY------------------------------------------------------------
    def anns_by_img_id(self, img_id: int) -> List:
        """
        Query all the annotations that belong to an image
        :param img_id: id of the image the annotations belong to
        :return: A list of annotations
        """
        return self.__session.query(Annotation).filter(Annotation.image_id == img_id).all()

    def ann_by_id(self, ann_id: int) -> Annotation:
        """
        Query one annotation defined by its id
        :param ann_id: id of the annotation
        :return: An annotation object
        """
        return self.__session.query(Annotation).filter(Annotation.id == ann_id).one_or_none()

    # DELETE------------------------------------------------------------
    def anns_delete_by_img_id(self, img_id: int) -> None:
        """
        Deletes all annotation objects identified by their img_id
        :param img_id: query argument
        """
        anns_list = self.anns_by_img_id(img_id)
        if anns_list:
            for annotation in anns_list:
                self.__session.delete(annotation)
            self.commit()
        else:
            print('No such image')

    def ann_delete_by_id(self, ann_id: int) -> None:
        """
        Deletes an annotation object identified by its id
        :param ann_id: query argument
        """
        ann = self.ann_by_id(ann_id)
        if ann:
            self.__session.delete(ann)
            self.commit()
        else:
            print('No such annotation')

    # RESOURCES------------------------------------------------------------
    def release_resources(self):
        """
        Releases the session object
        """
        if self.__session:
            self.__session.close()

    def commit(self):
        """
        Commits to the session
        """
        if self.__session:
            self.__session.commit()
