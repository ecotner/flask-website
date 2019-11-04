from functools import wraps, lru_cache
from time import time
from typing import Callable


def temp_lru_cache(maxsize, dt):
    def outer(func):
        f = lru_cache(maxsize)(func)

        @wraps(f)
        def inner(*args, **kwargs):
            if time() - inner.last_refresh > dt:
                f.cache_clear()
                inner.last_refresh = time()
            return f(*args, **kwargs)

        inner.last_refresh = 0
        return inner

    return outer
