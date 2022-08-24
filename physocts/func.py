"""
file: func.py
author: Nikolay S. Vasil'ev
description: functional tools
"""

from typing import Callable, Any, TypeVar
from functools import partial, reduce
from operator import is_not


X = TypeVar("X")
Y = TypeVar("Y")


def relax(*a, **k):
    del a, k


ident = lambda x: x


def apply_item(hlr: Callable[[X, Y], None], inst: X, itm: Y):
    """
    Apply handler `hlr` to an instance `inst` with item: `itm` and return `itm`;
    this is a convenient method to remove or apply some actions in lambda-style
    functions.
    """
    hlr(inst, itm)
    return itm


flip: Callable[[ Callable[[X, Y], Any] ], Callable[[Y, X], Any] ]
flip = lambda f: lambda x, y: f(y, x)


composite: Callable[..., Callable[[Any], Any]]
composite = lambda *fs: reduce( lambda g, f: lambda x: f(g(x)), fs[::-1], lambda x: x )


monad_do_maybe: Callable[..., Callable[[Any], Any]]
monad_do_maybe = lambda *fs: reduce(
    lambda g, f: lambda x: (lambda res: f(res) if not res is None else None)(g(x)),
    fs[::-1],
    lambda x: x)


ident = lambda x: x


is_not_none = partial(flip(is_not), None)


def test_monad_do_maybe():

    assert monad_do_maybe(
        lambda x: x*2,
        lambda x: x + 1,
        lambda x: x**2)(3) == 20, "success scenario"

    assert monad_do_maybe(
        lambda x: None,
        lambda x: None,
        lambda x: x**2)(3) is None, "computation failed scenario 1"

    assert monad_do_maybe(
        lambda x: x*2,
        lambda x: None,
        lambda x: x**2)(3) is None, "computation failed scenario 2"

    assert monad_do_maybe(
        lambda x: None,
        lambda x: None,
        lambda x: None)(3) is None, "computation failed scenario 3"
