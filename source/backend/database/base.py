from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event


class BaseConnection:

    def __init__(self, config):
        self.remote = config.get('remote')
        self.db_dialect = config.get('db_dialect')
        self.db_user = config.get('db_user')
        self.db_pwd = config.get('db_pwd')
        self.db_host = config.get('db_host')
        self.db_name = config.get('db_name')

        self.engine = create_engine(f'{self.db_dialect}://{self.db_user}:{self.db_pwd}@{self.db_host}/{self.db_name}',
                                    echo=False)
        if not self.remote:
            self.event_listen()
        self.session_maker = sessionmaker(bind=self.engine)
        self.session = self.session_maker()

    @staticmethod
    def _fk_pragma_on_connect(dbapi_con, con_record):
        dbapi_con.execute('pragma foreign_keys=ON')

    def event_listen(self):
        event.listen(self.engine, 'connect', self._fk_pragma_on_connect)


# local sqlite database for checking things
LOCAL_URL = 'sqlite:///secure_vision.db'
Base = declarative_base()
