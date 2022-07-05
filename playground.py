#!/usr/bin/python3
"""
playground
"""

from physocts import exceptions
from physocts import jsonlike

# exceptions.report_traceback()
# try:
#     raise Exception("lololo")
# except Exception:
#     print(exceptions.report_traceback())

d = {'a': 1, 'b': 2}
if not (res := jsonlike.write(d, "/lololo")):
    print(f"Failed to write file:\n{res.value}")
