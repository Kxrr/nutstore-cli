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
    'unix_join',
    'splitext',
    'NutPath',
)


class NutPath(object):
    def __init__(self, prefix='/dav', start='/'):
        self._prefix = prefix
        self._set_abs_dummy_path(start)

    def _set_abs_dummy_path(self, path):
        assert path.startswith('/')
        self.dummy_path = path

    def set_dummy_path(self, directory):
        self._set_abs_dummy_path(
            unix_join(self.dummy_path, directory)
        )

    def to_real_path(self, path):
        return '{0}{1}'.format(self._prefix, unix_join(self.dummy_path, path))

    @property
    def real_path(self):
        return self.to_real_path(self.dummy_path)

    def __str__(self):
        return '<NutPath "{}">'.format(self.real_path)


def unix_join(base, path, **kwargs):
    """
    Copied from http-prompt/http_prompt/execution.py

    >>>unix_join('a', '/b')
    "/b"

    >>>unix_join('a', 'b')
    "a/b"
    """
    if not base.endswith('/'):
        base += '/'
    url = urljoin(base, path, **kwargs)
    if url.endswith('/') and not path.endswith('/'):
        url = url[:-1]
    return url
