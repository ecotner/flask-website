from functools import wraps, lru_cache
from time import time
from typing import List
import re

########################################################################################
##                                Cacheing/performance                                ##
########################################################################################


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


########################################################################################
##                                   Form validation                                  ##
########################################################################################


def validate_tag(tag: str) -> bool:
    """Returns True if tag is valid, else false."""
    if re.fullmatch(r"[a-zA-Z0-9\-]+", tag):
        return True
    else:
        return False
