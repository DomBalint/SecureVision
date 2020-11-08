import json

from sqlalchemy import Column, Integer, String
from sqlalchemy import Sequence
from werkzeug.security import generate_password_hash

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


class UserHandler:

    def __init__(self, session_maker):
        self.__session = session_maker()

    def register_users(self, json_file_path):
        with open(json_file_path, 'r') as file:
            data = json.load(file)
            for employee in data['Users']:
                User.as_unique(self.__session, name=employee['name'],
                               user_pass=generate_password_hash(employee['pass'], 'sha256'),
                               user_rights=employee['rights'])
        self.__session.commit()

    def user_by_name(self, name):
        return self.__session.query(User).filter(User.name == name).one_or_none()

    def user_by_id(self, user_id):
        return self.__session.query(User).filter(User.id == user_id).one_or_none()

    def release_resources(self):
        if self.__session:
            self.__session.close()

    def commit(self):
        if self.__session:
            self.__session.commit()
