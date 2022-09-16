"""
file: func.py
author: Nikolay S. Vasil'ev
description: functional tools
"""

from typing import Callable, Any, TypeVar, Iterable, Optional, Union
from functools import partial, reduce
from operator import is_not, is_

from .either import Either, EitherType


T = TypeVar("T")
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


composite = lambda *fs: reduce( lambda g, f: lambda x: f(g(x)), fs[::-1], lambda x: x )

compose = composite


bind_maybes = lambda *fs: reduce(
    lambda g, f: lambda x: (lambda res: f(res) if not res is None else None)(g(x)),
    fs[::-1],
    ident)

bind_lists = lambda *fs: reduce(
    lambda g, f: lambda x: sum(list(map(f, g(x))), []),
    fs[::-1],
    ident)

bind_lists_ = lambda *fs: reduce(
    lambda g, f: lambda x: sum(list(map(f, g(x))), []),
    fs[::-1],
    lambda x: [x])

bind_eithers = lambda *fs: reduce(
    lambda g, f: lambda x: ( lambda res: f(res.value) if res else res )( g(x) ),
    fs[::-1],
    Either.right)

chain_either = lambda x, f: f(x.value) if x else x


is_not_none = partial(flip(is_not), None)
is_none = partial(flip(is_), None)


from .iter_ext import skip_while, maybe_head


coalesce: Callable[ [Iterable[Union[None, T]]], Optional[T] ]
coalesce = compose(maybe_head, partial(skip_while, is_none))


def test_bind_maybes():

    assert bind_maybes(
        lambda x: x*2,
        lambda x: x + 1,
        lambda x: x**2)(3) == 20, "success scenario"

    assert bind_maybes(
        lambda x: None,
        lambda x: None,
        lambda x: x**2)(3) is None, "computation failed scenario 1"

    assert bind_maybes(
        lambda x: x*2,
        lambda x: None,
        lambda x: x**2)(3) is None, "computation failed scenario 2"

    assert bind_maybes(
        lambda x: None,
        lambda x: None,
        lambda x: None)(3) is None, "computation failed scenario 3"

    assert bind_maybes(
        lambda x: x*2,
        lambda x: x + 1,
        lambda x: x**2)(None) is None, "computation failed scenario 4"

def test_bind_lists():

    assert bind_lists(
        lambda x: [x-1, x+1],
        lambda x: [x, x*10, x*100, x*1000],
        lambda x: [x, x*(-1)])([1]) \
    == [0, 2, 9, 11, 99, 101, 999, 1001, -2, 0, -11, -9, -101, -99, -1001, -999], \
    "computation success"

    assert bind_lists(
        lambda x: [x-1, x+1],
        lambda x: [],
        lambda x: [x, x*(-1)])([1]) == [], "computation failed scenario 1"

    assert bind_lists(
        lambda x: [x-1, x+1],
        lambda x: [x, x*10, x*100, x*1000],
        lambda x: [])([1]) == [], "computation failed scenario 2"

    assert bind_lists(
        lambda x: [],
        lambda x: [x, x*10, x*100, x*1000],
        lambda x: [x, x*(-1)])([1]) == [], "computation failed scenario 3"

    assert bind_lists(
        lambda x: [x-1, x+1],
        lambda x: [x, x*10, x*100, x*1000],
        lambda x: [x, x*(-1)])([]) \
    == [], \
    "computation failed scenario 4"

def test_bind_either():

    assert bind_eithers(Either.right)(1) == Either.right(1)

    assert bind_eithers(
        lambda x: Either.right(x+1),
        lambda x: Either.right(x*10),
        lambda x: Either.right(x*(-1)))(1) \
    == Either.right(-9)

    assert bind_eithers(
        lambda x: Either.left("error 1"),
        lambda x: Either.right(x*10),
        lambda x: Either.right(x*(-1)))(1) \
    == Either.left("some error")

    assert bind_eithers(
        lambda x: Either.right(x+1),
        lambda x: Either.left("error 2"),
        lambda x: Either.right(x*(-1)))(1) \
    == Either.left("some error")

    assert bind_eithers(
        lambda x: Either.right(x+1),
        lambda x: Either.right(x*10),
        lambda x: Either.left("error 3"))(1) \
    == Either.left("some error")

def test_coalesce():
    """testing coalesce function"""

    assert coalesce([1,2,3]) == 1
    assert coalesce([None, 2, 3]) == 2
    assert coalesce([None, None, 3]) == 3
    assert coalesce([]) is None
