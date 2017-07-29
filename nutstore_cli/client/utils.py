# coding: utf-8
import inspect
import os

from nutstore_cli.client.exceptions import FileNotExistException


def get_attr(obj, attr_or_fn):
    if isinstance(attr_or_fn, basestring):
        return getattr(obj, attr_or_fn)
    elif callable(attr_or_fn):
        return attr_or_fn(obj)
    else:
        raise TypeError(type(attr_or_fn))


def check_local_path(func):
    def deco(*args, **kwargs):
        arguments = inspect.getcallargs(func, *args, **kwargs)
        local_path = arguments.get('local_path')
        if local_path and not os.path.exists(local_path):
            raise FileNotExistException.make_exception(local_path)
        return func(*args, **kwargs)

    return deco