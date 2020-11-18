from dependency_injector import providers, containers
from sqlalchemy.orm import sessionmaker

from SecureVision.source.backend.database.annotation import AnnotationHandler
from SecureVision.source.backend.database.camera import CameraHandler
from SecureVision.source.backend.database.feedback import FeedbackHandler
from SecureVision.source.backend.database.image import ImageHandler
from SecureVision.source.backend.database.user import UserHandler
from base import BaseConnection


class AttributeFactory(providers.Provider):
    __slots__ = ('_factory',)

    def __init__(self, *args, **kwargs):
        self._factory = providers.Factory(*args, **kwargs)
        super().__init__()

    def __deepcopy__(self, memo):
        copy = providers.deepcopy(self._factory, memo)
        return self.__class__(
            copy.provides,
            *copy.args,
            **copy.kwargs,
        )

    def __getattr__(self, item):
        return providers.Callable(getattr, self._factory, item)

    def _provide(self, args, kwargs):
        return self._factory(*args, **kwargs)


class Configs(containers.DeclarativeContainer):
    config = providers.Configuration('config')
    # TODO: BETTER PLACE FOR CONFIG READER
    config.override({
        "remote": True,
        "db_dialect": "postgresql",
        "db_user": "vmnaxxcjwwqlkc",
        "db_pwd": "a20d0f30efe4cf8a8acab7d6204e6f0f2652cdaf36dc1a79a636b4f9a317fb88",
        "db_host": "ec2-54-228-209-117.eu-west-1.compute.amazonaws.com",
        "db_name": "d45rfoe1nssprp",
    })


class Databases(containers.DeclarativeContainer):
    base_connection = AttributeFactory(BaseConnection, config=Configs.config)
    base_session_maker = base_connection.session_maker()
    base_engine = base_connection.engine()
    # GLOBAL SESSION
    base_session = base_connection.session()


class Handlers(containers.DeclarativeContainer):
    user_handler = providers.Factory(UserHandler, session=Databases.base_session_maker())
    cam_handler = providers.Factory(CameraHandler, session=Databases.base_session_maker())
    img_handler = providers.Factory(ImageHandler, session=Databases.base_session_maker())
    ann_handler = providers.Factory(AnnotationHandler, session=Databases.base_session_maker())
    fb_handler = providers.Factory(FeedbackHandler, session=Databases.base_session_maker())
