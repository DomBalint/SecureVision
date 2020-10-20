from sqlalchemy import Column, Integer, String
from sqlalchemy import Sequence

from SecureVision.source.backend.database.base import Base


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(100))
    user_pass = Column(String(50))
    user_rights = Column(Integer)
    num_feedback = Column(Integer)

    def __repr__(self):
        return "<User(name='%s', user_rights='%d')>" % (self.name, self.user_rights)
