import logging

logger = logging.getLogger(__name__)


def log_any_exception(log=logger):
    """
    Wraps function in try - except Exception
    In except block logs any exception with level error
    Pass logger to correctly locate exception source
    """

    def wrap_func(func):
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except Exception as e:
                log.error(e)
                log.exception(e)

        return wrapper

    return wrap_func
