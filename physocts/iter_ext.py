"""
file: iter_ext.py
author: Nikolay S. Vasil'ev
description: additional tools for iterators
"""
from typing import List, Dict, Tuple, Any, Set, Optional, Callable, FrozenSet, Iterable, TypeVar

from functools import partial
from more_itertools import take

from .func import bind_maybes

T = TypeVar("T")

def skip_while(pred: Callable[[T], T], xs: Iterable[T]) -> Iterable[T]:
    """skip iterables while predicate is true"""
    for i, x in enumerate(xs):
        if not pred(x):
            return iter(xs[i:])
    return iter([])


maybe_head: Callable[ [Iterable[T]], Optional[T] ]
maybe_head = bind_maybes(
    lambda x: x[0] if x else None,
    partial(take, 1))


def test_maybe_head():
    """tests"""
    assert maybe_head(iter([1,2,3])) == 1
    assert maybe_head(iter([])) is None
    assert maybe_head([1,2,3]) == 1
    assert maybe_head([]) is None
    assert maybe_head({1,2,3}) in [1, 2, 3]
    assert maybe_head(set()) is None


def test_skipWhile():
    """testing skipWhile function"""

    assert list(skip_while(lambda x: x>0, [1,2,3, -1,3,2])) == [-1,3,2]
    assert list(skip_while(lambda x: x>0, [1,2,3])) == []
    assert list(skip_while(lambda x: x>0, [-1,-2,-3])) == [-1, -2, -3]
