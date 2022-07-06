#!/usr/bin/python3
"""
playground
"""

from physocts import log
from physocts import exceptions
from physocts import json_ext

LOG = log.get_logger()
LOG.setLevel(1)
log.enable_stderr(1)

# exceptions.report_traceback()
# try:
#     raise Exception("lololo")
# except Exception:
#     print(exceptions.report_traceback())

d = {'a': 1, 'b': 2}
# if not (res := json_ext.write(d, "lololo")):
#     LOG.error("Failed to write file:\n%s", res.value)

if not (res := json_ext.load("./lololo")):
    LOG.error("Failed to load file:\n%s", res.value)
else:
    json_ext.info(res.value)
    d = res.value
    d = {1,2,3}
    LOG.info(json_ext.flat(d).value)
    LOG.info(json_ext.pretty(d).value)
