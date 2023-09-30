from django.conf import settings

nothrow_registry = []


def func_nothrow(throwing_func, register=True):
    """
    Get a modified version of function which does not throw exceptions.
    if not in debugging mode

    register - register to global variable to prevent from being purged.
    """

    def wrapped(*args, **kwargs):
        if settings.DEBUG:
            return throwing_func(*args, **kwargs)
        else:
            try:
                return throwing_func(*args, **kwargs)
            except:  # noqa
                # TODO: Log error
                return None

    if register:
        nothrow_registry.append(wrapped)

    return wrapped
