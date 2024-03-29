"""
file: dict_ext.py
author: Nikolay S. Vasil'ev
descriptions: some methods for dict instances
"""
from typing import Callable, Optional, Any
from functools import partial
from .func import flip, bind_maybes

maybe_getter: Callable[ [str], Callable[ [dict], Optional[Any] ]]
maybe_getter = lambda key: bind_maybes(
    partial(flip(dict.get), key),
    lambda x: x if isinstance(x, dict) else None)

maybe_getter_chain = lambda *keys: bind_maybes(*[maybe_getter(key) for key in keys[::-1]])


def dict_join(x, y=None):
    """Concatenate two dictionaries.

    Use this method to join two dictionaries when simple `update` not working
    properly as shown bellow:

        >>> x = {'d': 1, 'a': {'aa': 11, 'ab': 12}, 'b': 2}
        >>> y = {'d': 1, 'a': {'ab': -12}, 'c': 3}
        >>> {**x, **y}
        {'a': {'ab': -12}, 'b': 2, 'c': 3}
        >>> dict_join(x, y)
        {'a': 1, 'a': {'aa': 11, 'ab': -12}, 'b': 2, 'c': 3}

    Overlapping keys will be overwritten with y key values.
    If y is None, than x will be returned.

    Arguments:
        x: first dictionary to be concatenated
        y: second dictionary to be concatenated or None

    Returns:
        concatenated dictionary
    """
    assert isinstance(x, dict)
    if not y:
        return x
    assert isinstance(y, dict), "y not a dict: type = " + repr(type(y))
    overlap_keys = x.keys() & y.keys()
    if not overlap_keys:
        return {**x, **y}
    # log_hlr("Got overlap keys: %r", overlap_keys)
    out_dct = dict()

    # first update output dictionary with unoverlaped keys
    out_dct.update({c_key: x[c_key] for c_key in x.keys() - y.keys()})
    out_dct.update({c_key: y[c_key] for c_key in y.keys() - x.keys()})
    # log_hlr("Output with unoverlaped keys: %r", out_dct)

    # recursively update overlaped keys
    for c_key in overlap_keys:
        # log_hlr("Processing key: %r", c_key)
        if isinstance(x[c_key], dict):
            if not isinstance(y[c_key], dict):
                raise TypeError("Key %r items type do not match: " % c_key \
                                + "%r <---> %r" % (x[c_key], y[c_key]))
            # log_hlr("Overlaping dictionaries: %r and %r", x[c_key], y[c_key])
            out_dct.update({c_key: dict_join(x[c_key], y[c_key])})
            # return out_dct
            continue
        # replace x[c_key] with y[c_key]
        # log_hlr("Overlaping item of x=%r with y=%r", x[c_key], y[c_key])
        out_dct.update({c_key: y[c_key]})

    # log_hlr("Output: %r", out_dct)
    return out_dct


def test_maybe_getter_chain():

    assert maybe_getter_chain()({'a':1}) == {'a':1}
    assert maybe_getter_chain('a')({'b':1}) is None
    assert maybe_getter_chain('a')({'a':None}) is None
    assert maybe_getter_chain('a')({'a':1}) == 1
    assert maybe_getter_chain('a', 'b')({'c':1}) is None
    assert maybe_getter_chain('a', 'b')({'a':1}) is None
    assert maybe_getter_chain('a', 'b')({'a':None}) is None
    assert maybe_getter_chain('a', 'b')({'a':{'c':1}}) is None
    assert maybe_getter_chain('a', 'b')({'a':{'b':None}}) is None
    assert maybe_getter_chain('a', 'b')({'a':{'b':1}}) == 1
    assert maybe_getter_chain('a', 'b', 'c')({'a':{'b':{'c':1}}}) == 1
