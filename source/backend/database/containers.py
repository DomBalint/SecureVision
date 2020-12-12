from dependency_injector import providers, containers

from database.annotation import AnnotationHandler
from database.camera import CameraHandler
from database.feedback import FeedbackHandler
from database.image import ImageHandler
from database.user import UserHandler
from database.base import BaseConnection


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
    # config.override({
    #     "remote": True,
    #     "db_dialect": "postgresql",
    #     "db_user": "gixvhnjqlweyta",
    #     "db_pwd": "1ee75b62d9b9e840482eadf7d0e11d2a35ea8c226275d21d3073da65c83ad94a",
    #     "db_host": "ec2-54-247-79-178.eu-west-1.compute.amazonaws.com",
    #     "db_name": "der4mdbrf62is8",
    # })

    config.override({
        "remote": True,
        "db_dialect": "postgresql",
        "db_user": "admin",
        "db_pwd": "SecureVision123",
        "db_host": "192.168.1.104:5432",
        "db_name": "predictions",
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
