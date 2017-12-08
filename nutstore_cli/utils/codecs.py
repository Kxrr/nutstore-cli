# coding: utf-8
from __future__ import absolute_import
import logging

logger = logging.getLogger(__name__)


__all__ = (
    'to_str',
    'to_unicode'
)


def to_str(s):
    if isinstance(s, str):
        return s
    elif isinstance(s, unicode):
        return s.encode('utf-8')
    elif s is None:
        return None
    else:
        raise UnicodeEncodeError('can\'t encode "{}" to "str" '.format(type(s)))


def to_unicode(s):
    if isinstance(s, unicode):
        return s
    elif isinstance(s, str):
        return s.decode('utf-8')
    elif s is None:
        return None
    else:
        raise UnicodeDecodeError('can\'t convert "{}" to "unicode" '.format(type(s)))
