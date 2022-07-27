"""
file: wrappers.py
author: Nikolay S. Vasil'ev
description: wrappers for functions and classes
"""

from functools import wraps
from typing import Callable, TypeVar
from typing_extensions import ParamSpec

from physocts.either import Either, EitherType
from physocts.exceptions import report_traceback

T = TypeVar('T')
P = ParamSpec('P')


def wrap_in_either(f: Callable[P, T]) -> Callable[P, EitherType[T]]:
    """
    Wraps a function in try-except statement, returning result in Right instance
    on success and a trace report string in Left instance
    """

    @wraps(f)
    def g(*a, **k):
        try:
            res = f(*a, **k)
        except SystemExit:
            raise
        except:  # pylint: disable=W0702
            return Either.left(report_traceback())

        return Either.right(res)

    return g
