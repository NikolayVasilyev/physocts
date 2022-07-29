"""
file: random.py
author: Nikolay S. Vasil'ev
description: a collection of functions which have random behavior
"""
import string
from secrets import choice
from functools import partial


def _f(flag: int, k: int):
    """returns a random string of length `k`"""
    return "".join([choice(\
        (string.ascii_lowercase if (flag & 1) else "") + \
        (string.ascii_uppercase if (flag & 2) else "") + \
        (string.digits if (flag & 4) else "") + \
        (string.punctuation if (flag & 8) else "")) for i in range(k)])

letters_lower = partial(_f, 1)
letters_upper = partial(_f, 2)
letters = partial(_f, 3)
digits = partial(_f, 4)
digits_and_letters = partial(_f, 7)
printable = partial(_f, 15)
