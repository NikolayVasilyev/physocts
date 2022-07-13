"""
file: either.py
author: Nikolay S. Vasil'ev
description: implementation for Either class, that may have two `values`
    either left or right; left is used for error instance, and right is for
    correct values
"""

from typing import TypeVar, Generic, Union, Any


def not_implemented(*a, **k):
    """Throw not impolemented error"""
    raise NotImplementedError


class LeftRight:
    """Base class for Left and Right"""

    value = property(not_implemented)

    def __bool__(self):
        return not_implemented()


class Left(LeftRight):
    """Class instance holds an error"""

    value = property(lambda obj: obj._err)

    def __init__(self, err: str):
        self._err = err

    def __bool__(self):
        return False


T = TypeVar('T')

class Right(LeftRight, Generic[T]):
    """Class insance holds a return value"""

    value = property(lambda obj: obj._value)

    def __init__(self, value: T):
        self._value = value

    def __bool__(self):
        return True


EitherType = Union[Left, Right[T]]


class Either:
    """Either meta class, see module doc string"""

    def __init__(self, *a, **k):
        raise NotImplementedError("Either method is not supposed to be used as an instance")

    @staticmethod
    def left(err: str) -> Left:
        """Create a new Left class instance"""
        return Left(err)

    @staticmethod
    def right(value: Any) -> Right:
        """Create a new Right class instance"""
        return Right(value)
