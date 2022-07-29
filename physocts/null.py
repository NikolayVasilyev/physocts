"""
file: null.py
author: Nikolay S. Vasil'ev
description: implementations for `null` abstraction
"""

class Null:

    """All attrubutes getter, all functions with all signatures executer"""

    def __init__(self, clbl=None):

        self.clbl = clbl or (lambda *a, **k: None)

    def __call__(self, *a, **k):

        self.clbl((a, k))

        return Null(self.clbl)

    def __getattr__(self, name):

        self.clbl(name)

        return Null(self.clbl)

    def __bool__(self):

        return False

    def __str__(self):

        return "null"
