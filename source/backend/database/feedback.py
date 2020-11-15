from sqlalchemy import Column, Integer, Boolean
from sqlalchemy import ForeignKey
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref

from SecureVision.source.backend.database.base import Base


class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, Sequence('feedback_id_seq'), primary_key=True)
    correct_detection = Column(Boolean, nullable=True)
    # TODO as it is a one to one mapping should image id be unique? check
    image_id = Column(Integer, ForeignKey('image.id'), nullable=False)
    image = relationship("Image", backref=backref("feedback", uselist=False))

    def __repr__(self):
        return "<Feedback(id='%s', obj_type='%s')>" % (self.id, self.correct_detection)


class FeedbackHandler:

    def __init__(self, session_maker):
        self.__session = session_maker()

    # ADD------------------------------------------------------------
    def add_fb(self, img_id: int, det_correct: bool) -> None:
        """
        Add a Feedback to the database
        :param det_correct: Boolean value if the detection (all the annotations) are correct or not
        :param img_id: id of the image the feedback belongs to
        """
        fb = Feedback(correct_detection=det_correct, image_id=img_id)
        self.__session.add(fb)
        self.commit()

    def update_create_fb_by_img_id(self, img_id: int, new_value: bool) -> bool:
        """
        Update the feedback by its img_id (as that is unique)
        :param img_id: query argument
        :param new_value: new Boolean value
        :returns: boolean value if successful or not
        """
        fb = self.fb_by_img_id(img_id)
        if fb:
            fb.correct_detection = new_value
            self.commit()
            return True
        else:
            self.add_fb(img_id=img_id, det_correct=new_value)
            return True

    # UPDATE------------------------------------------------------------
    def update_fb_by_img_id(self, img_id: int, new_value: bool) -> bool:
        """
        Update the feedback by its img_id (as that is unique)
        :param img_id: query argument
        :param new_value: new Boolean value
        :returns: boolean value if successful or not
        """
        fb = self.fb_by_img_id(img_id)
        if fb:
            fb.correct_detection = new_value
            self.commit()
            return True
        else:
            print('No such feedback')
            return False

    def update_fb_by_fb_id(self, fb_id: int, new_value: bool) -> bool:
        """
        Update the feedback by its id
        :param fb_id: query argument
        :param new_value: new Boolean value
        :returns: boolean value if successful or not
        """
        fb = self.fb_by_id(fb_id)
        if fb:
            fb.correct_detection = new_value
            self.commit()
            return True
        else:
            print('No such feedback')
            return False

    # QUERY------------------------------------------------------------
    def fb_by_img_id(self, img_id: int) -> Feedback:
        """
        Queries the feedbacks and searches by img id (the image it belongs to)
        :param img_id: query argument, image the feedback belongs to
        :return: Feedback obj that satisfies the query
        """
        return self.__session.query(Feedback).filter(Feedback.image_id == img_id).one_or_none()

    def fb_by_id(self, fb_id: int) -> Feedback:
        """
       Queries the feedbacks and searches by fb_id
       :param fb_id: query argument
       :return: Feedback obj that satisfies the query
       """
        return self.__session.query(Feedback).filter(Feedback.id == fb_id).one_or_none()

    # DELETE------------------------------------------------------------
    def fb_delete_by_img_id(self, img_id: int) -> None:
        """
        Deletes the feedback that satisfies the query, identified by its img_id
        :param img_id: query argument, image the feedback belongs to
        """
        fb = self.fb_by_img_id(img_id)
        if fb:
            self.__session.delete(fb)
            self.commit()
        else:
            print('No such feedback')

    def fb_delete_by_id(self, fb_id: int) -> None:
        """
        Deletes the feedback that satisfies the query, identified by its id
        :param fb_id: query argument
        """
        fb = self.fb_by_id(fb_id)
        if fb:
            self.__session.delete(fb)
            self.commit()
        else:
            print('No such feedback')

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
