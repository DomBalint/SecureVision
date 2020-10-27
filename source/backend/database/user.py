from sqlalchemy import Column, Integer, String
from sqlalchemy import Sequence

from SecureVision.source.backend.database.base import Base
from SecureVision.source.backend.database.unique import UniqueMixin
from SecureVision.source.backend.database.unique import _unique


class User(UniqueMixin, Base):
    __tablename__ = 'user'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    user_pass = Column(String(50), nullable=False)
    user_rights = Column(Integer, nullable=False)
    num_feedback = Column(Integer, nullable=True)

    @classmethod
    def unique_hash(cls, name):
        return name

    @classmethod
    def unique_filter(cls, query, name):
        return query.filter(User.name == name)

    @classmethod
    def as_unique(cls, session, **kw):
        return _unique(
                    session,
                    cls,
                    cls.unique_filter,
                    cls,
                    kw,
                    'name'
               )

    def __repr__(self):
        return "<User(name='%s', user_rights='%d')>" % (self.name, self.user_rights)
