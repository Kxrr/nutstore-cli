# coding: utf-8
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


