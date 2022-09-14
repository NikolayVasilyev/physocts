"""
file: either.py
author: Nikolay S. Vasil'ev
description: implementation for Either class, that may have two `values`
    either left or right; left is used for error instance, and right is for
    correct values
"""

from typing import TypeVar, Generic, Union, Any, Type
from dataclasses import dataclass


def not_implemented(*a, **k):
    """Throw not impolemented error"""
    raise NotImplementedError


@dataclass
class Error:
    """collect info about an exception"""
    error: Type[Exception]
    trace: str
    msg: str


class LeftRight:
    """Base class for Left and Right"""

    value = property(not_implemented)

    __bool__ = not_implemented

    __eq__ = not_implemented


class Left(LeftRight):
    """Class instance holds an error"""

    value = property(lambda obj: obj._err)

    def __init__(self, err: Union[str, Error]):
        self._err = err

    def __bool__(self):
        return False

    def __eq__(self, other):
        return True


T = TypeVar('T')

class Right(LeftRight, Generic[T]):
    """Class insance holds a return value"""

    value = property(lambda obj: obj._value)

    def __init__(self, value: T):
        self._value = value

    def __bool__(self):
        return True

    def __eq__(self, other):
        return isinstance(other, Right) and (other.value == self.value)


EitherType = Union[Left, Right[T]]


class Either:
    """Either meta class, see module doc string"""

    __init__ = not_implemented
    # def __init__(self, *a, **k):
    #     raise NotImplementedError("Either class is not supposed to be used as an instance")

    @staticmethod
    def left(err: Union[str, Error]) -> Left:
        """Create a new Left class instance"""
        return Left(err)

    @staticmethod
    def right(value: Any) -> Right:
        """Create a new Right class instance"""
        return Right(value)
