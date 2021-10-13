"""Decorator methods"""

from functools import wraps
from time import sleep


def retry(exec, retries=3, delay=15):
    """Retry decorator - : param exec: the Exception to catch"""
    def dec_try(f):
        """Retry decorator"""
        @wraps(f)
        def f_try(*args, **kwargs):
            """try calling the func"""
            for _ in range(0, retries):
                try:
                    return f(*args, **kwargs)
                except exec:
                    sleep(delay)

                return f(*args, **kwargs)

        return f_try

    return dec_try
