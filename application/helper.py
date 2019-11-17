from functools import wraps, lru_cache
from time import time
from typing import List
import re
import os

########################################################################################
##                                Cacheing/performance                                ##
########################################################################################


def temp_lru_cache(maxsize=1, dt=60):
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
##                       Form validation, password hashing                            ##
########################################################################################


def hash_password(pw: str, salt: str, it: int):
    """Recursively hashes a given password.

    Uses the SHA-256 algorithm to hash a password + salt, then takes the generated
    hash (encoded as a hex string -> bytes object), and iteratively applies the
    hashing algorithm again for <it> iterations.
    """
    import hashlib

    for _ in range(it):
        pw = hashlib.sha256(bytes(salt + pw, "utf-8")).hexdigest()
    return pw


def hashpw(password: str, username: str):
    """
    Simplifies the hashing procedure so you just need to provide the password
    and username, and the salt and # of iterations are produced from environment
    variables.
    """
    return hash_password(
        pw=password,
        salt=(os.environ["PW_SALT"] + username),
        it=int(os.environ["PW_HASHING_ITERATIONS"]),
    )


def validate_tag(tag: str) -> bool:
    """Returns True if tag is valid, else false."""
    if re.fullmatch(r"[a-zA-Z0-9\-]+", tag):
        return True
    else:
        return False
