# coding: utf-8
from __future__ import absolute_import

import logging
import tempfile

logger = logging.getLogger(__name__)

__all__ = (
    'hfloat',
    'humanbytes',
    'save_text'
)

UNITS = (
    (2 ** 30.0, 'GB'),
    (2 ** 20.0, 'MB'),
    (2 ** 10.0, 'KB'),
    (0.0, 'b'),)


def hfloat(f, p=5):
    """Convert float to value suitable for humans.

    Arguments:
        f (float): The floating point number.
        p (int): Floating point precision (default is 5).

    Copied from celery
    """
    i = int(f)
    return i if i == f else '{0:.{p}}'.format(f, p=p)


def humanbytes(s):
    """Convert bytes to human-readable form (e.g., KB, MB).

    Copied from celery
    """
    return next(
        '{0}{1}'.format(hfloat(s / div if div else s), unit)
        for div, unit in UNITS if s >= div
    )


def save_text(s, dest=None):
    dest = dest or tempfile.mktemp(suffix='.log')
    with open(dest, 'w') as g:
        g.write(s)
    return dest
