"""
file: meta.py
author: Nikolay S. Vasil'ev
description: meta types

TODO: root dictionary keys are not changed when dict(inst) has changed
"""

import copy
import jsonschema
from functools import partial

from .log import get_logger
from .func import relax
from .dict_ext import dict_join

def validator(schema, log_hlr, x):
    """Returns True if valid, False otherwise"""

    try:
        jsonschema.validate(x, schema)

    except jsonschema.ValidationError as err:
        log_hlr("Validation error: \n%s", err)
        return False

    return True


LOG = get_logger()


META_INST_NAME = "CustomData"


class DataMeta:
    """Data meta class, used to validate and simplify work with dictionaries
    >>> cur_schema = {
            "type": "object",
            "properties": {
                "a": {
                    "type": "object",
                    "properties": {
                        "b": {
                            "type": "object",
                            "properties": {
                                "c": {"type": "string"}}}}}}}
    >>> d = MetaData(cur_schema)({"a": {"b": {"c": 1}}})
    >>> d.a
    >>> d.a.b
    >>> dict(d)
    >>> dict(d.a)
    >>> dict(d.a.b)
    >>> d.valid
    >>> dict(d))
    >>> d.a.b.c = "one"
    >>> dict(d)
    """
    def cls_init(obj, data=None):  # pylint: disable=E0213
        """A new type constructor"""
        data = data or dict()
        assert isinstance(data, dict), "Data given is not a dictionary: %r" % repr(data)


        # This should prevent side-effects from external references to the
        # default data instance.
        try:
            default_data = copy.deepcopy(obj._default_data)  # pylint: disable=E1101
        except TypeError as err:
            LOG.warning("Invalid data given, failed to deepcopy: \"%r\"", err)
            raise err

        # `keys` key is required to convert to a dictionary.
        if "keys" in data.keys():
            raise KeyError("Data confilict: key: `keys`")

        cur_data = dict_join(default_data, data)

        obj._data = cur_data  # pylint: disable=W0201

    def cls_init_no_copy(obj, data):  # pylint: disable=E0213
        """A new type constructor"""
        obj._data = data  # pylint: disable=W0201

    def cls_validate(obj):  # pylint: disable=E0213
        """Validate object data using a custom validator"""
        return obj._validator(obj._data)  # pylint: disable=E1101

    def cls_getitem(obj, key):  # pylint: disable=E0213
        return obj._data[key]

    def cls_getattr(obj, name):  # pylint: disable=E0213
        # print("getattr: %r" % name)
        cur_dict = obj._data
        if not name in cur_dict.keys():
            return None
        data = cur_dict[name]
        if not isinstance(data, dict):
            return data
        return type(META_INST_NAME, (object, ),
                    {**DataMeta.METHODS, "__init__": DataMeta.cls_init_no_copy})(data)

    def cls_setattr(obj, key, value):  # pylint: disable=E0213
        # print("cls_setattr, key=%r, value=%r" % (key, value))
        if key[0] == "_":
            obj.__dict__[key] = value
            return
        if type(value).__name__ == META_INST_NAME:
            obj._data[key] = value._data  # pylint: disable=W0212
            return
        obj._data[key] = value

    def cls_deepcopy(obj, memo):  # pylint: disable=E0213, disable=W0613
        obj.__dict__ = copy.deepcopy(obj.__dict__)
        return obj

    METHODS = {
        "__getattr__": cls_getattr,
        "__setattr__": cls_setattr,
        "__getitem__": cls_getitem,
        "__deepcopy__": cls_deepcopy,
        "keys": lambda obj: obj._data.keys()}  # pylint: disable=W0212

    def __new__(cls, schema=None, default_data=None):
        """
        Create a new type.

        Arguments:
            default_data: (dict) a dictionary, must match the schema,
            must comply deepcopy
        """
        schema = schema or dict()
        default_data = default_data or dict()

        assert isinstance(schema, dict)

        # Get a new type name from schema's ID
        # assert isinstance(schema, dict), "Schema must be a dictionary"
        # name = schema.get("title", "Unknown")
        # assert isinstance(name, str), "Schema's ID must be a string"
        # name = "Data%s" % name
        name = META_INST_NAME


        vldtr = partial(validator, schema, LOG.warning)

        bases = (object, )

        dct = {
            **DataMeta.METHODS,
            "__init__": DataMeta.cls_init,
            "_default_data": default_data,
            "_schema": schema,
            "_validator": staticmethod(vldtr),
            "schema": property(lambda cls: cls._schema),
            "validator": property(lambda cls: cls._validator),
            "__bool__": DataMeta.cls_validate}

        return type(name, bases, dct)

def test_meta_data_object():
    """Testing meta data objects"""

if __name__ == "__main__":
    test_meta_data_object()
