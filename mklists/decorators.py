"""Decorators"""

import os
from functools import wraps


def preserve_cwd(function):
    """Decorate a function so that changes of directory will not persist."""

    @wraps(function)
    def decorator(*args, **kwargs):
        cwd = os.getcwd()
        try:
            return function(*args, **kwargs)
        finally:
            os.chdir(cwd)

    return decorator
