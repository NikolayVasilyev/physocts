"""
file: wrappers.py
author: Nikolay S. Vasil'ev
description: wrappers for functions and classes
"""

from typing import Callable, TypeVar, Optional
from functools import wraps, partial
from typing_extensions import ParamSpec

from .either import Either, EitherType, Error
from .exceptions import report_traceback
from .log import get_logger

LOG = get_logger()

T = TypeVar('T')
P = ParamSpec('P')


def wrap_in_either(f: Callable[P, T]) -> Callable[P, EitherType[T]]:
    """
    Wraps a function in try-except statement, returning result in Right instance
    on success and a trace report string in Left instance;
    SystemExit is a special case, this exception is re-raised.
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


def wrap_in_either_2(f: Callable[P, T]) -> Callable[P, EitherType[T]]:
    """
    Wraps a function in try-except statement, returning result in Right instance
    on success and an Error instance in Left instance;
    SystemExit is a special case, this exception is re-raised.
    """

    @wraps(f)
    def g(*a, **k):
        try:
            res = f(*a, **k)
        except SystemExit:
            raise
        except Exception as err:  # pylint: disable=W0703
            return Either.left(
                Error(
                    type(err),
                    report_traceback(),
                    str(err)))

        return Either.right(res)

    return g


def try_evaluate(on_err: Callable[[str], None], default: T) -> Callable[ [Callable[P, T]], Callable[P, T] ]:

    def wrapper(f: Callable[P, T]) -> Callable[P, T]:

        rtype = type(default)

        @wraps(f)
        def g(*a, **k) -> T:

            try:
                res = f(*a, **k)
            except:
                on_err(f"Call {f} with args: {a}, {k}\n" + report_traceback())
                return default

            assert isinstance(res, rtype), f"function call result is not of type: {rtype}"

            return res

        return g

    return wrapper

try_list = try_evaluate(LOG.warning, [])
try_dict = try_evaluate(LOG.warning, {})


OrDefaultWrapperType = Callable[ [Callable[P, Optional[T]]], Callable[P, T]]
def or_default(default: T) -> OrDefaultWrapperType:
    """WRITEME"""
    wrapper: OrDefaultWrapperType
    def wrapper(f):

        succes_type = type(default)

        @wraps(f)
        def g(*a, **k) -> T:

            res = f(*a, **k)

            if res is None:
                return default

            assert \
                isinstance(res, succes_type), \
                f"function call: {f} result: {type(res)} is not of type: {succes_type}"

            return res

        return g

    return wrapper


or_empty_list = or_default([])
