def _unique(session, cls, queryfunc, constructor, kw, unique_key='name'):
    """
    Checks if a class instance is unique or not, only for those classes which have unique attributes
    Like the User name and Image img_path
    :param session: Session object
    :param cls: Class object
    :param queryfunc: The query that gets the unique value
    :param constructor: Constructor function, currently default
    :param kw: Arguments, please use key worded
    :param unique_key: the name of the unique attribute
    :return:
    """
    cache = getattr(session, '_unique_cache', None)
    if cache is None:
        session._unique_cache = cache = {}

    key = (cls, kw.get(unique_key))
    if key in cache:
        print(f'The {kw.get(unique_key)} {unique_key} is not unique, try something else!')
        return cache[key]
    else:
        with session.no_autoflush:
            q = session.query(cls)
            q = queryfunc(q, kw.get(unique_key))
            obj = q.first()
            if not obj:
                obj = constructor(**kw)
                session.add(obj)
            else:
                print(f'The {obj.name} {unique_key} is not unique, try something else!')
        cache[key] = obj
        return


class UniqueMixin(object):

    @classmethod
    def unique_filter(cls, query, key):
        raise NotImplementedError()

    @classmethod
    def as_unique(cls, session, **kw):
        raise NotImplementedError()

