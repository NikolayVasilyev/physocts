"""
testing physocts.jsonlike module
"""

from physocts import jsonlike

def test():
    d = {'a':1, 'b':2}
    assert jsonlike.flat(d) == '{"a": 1, "b": 2}'
    assert jsonlike.pretty(d) == '{\n    "a": 1,\n    "b": 2\n}'
    
