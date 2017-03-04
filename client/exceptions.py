# coding: utf-8
import os
import inspect
from easywebdav.client import WebdavException


class NutStoreClientException(WebdavException):
    pass


class LocalException(NutStoreClientException):
    pass


class CloudException(NutStoreClientException):
    pass


class FileNotExistException(LocalException):

    @classmethod
    def make_exception(cls, path):
        return cls('The path <{}> does not exist on your machine.'.format(path))


def check_local_path(func):
    def deco(*args, **kwargs):
        arguments = inspect.getcallargs(func, *args, **kwargs)
        local_path = arguments.get('local_path')
        if local_path and not os.path.exists(local_path):
            raise FileNotExistException.make_exception(local_path)
        return func(*args, **kwargs)

    return deco
