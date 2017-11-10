# coding: utf-8
from os.path import (
    join,
    basename,
    splitext,
)
from urlparse import urljoin

__all__ = (
    'join',
    'basename',
    'path_resolve',
    'splitext',
    'PathHelper',
)


class PathHelper(object):
    """A helper that wraps pretty remote path to real dav path"""

    def __init__(self, prefix='/dav', start='/'):
        assert start.startswith('/')
        self._prefix = prefix
        self.pretty = start

    def cd(self, directory):
        self.pretty = path_resolve(self.pretty, directory)
        assert self.pretty.startswith('/')

    def _real_getter(self):
        return self.to_real(self.pretty)

    real = property(_real_getter)

    def to_real(self, path):
        return '{0}{1}'.format(self._prefix, path_resolve(self.pretty, path))

    def __str__(self):
        return '<NutPath "{}">'.format(self.real)


def path_resolve(base, path, **kwargs):
    """
    Copied from http-prompt/http_prompt/execution.py

    >>>path_resolve('a', '/b')
    "/b"

    >>>path_resolve('a', 'b')
    "a/b"
    """
    if not base.endswith('/'):
        base += '/'
    url = urljoin(base, path, **kwargs)
    if url.endswith('/') and not path.endswith('/'):
        url = url[:-1]
    return url
