# coding: utf-8
from __future__ import absolute_import

import os
import click

__all__ = (
    'info',
    'error',
    'echo',
    'debug',
)


def info(s):
    click.secho(s, fg='cyan')


def error(s):
    click.secho(s, fg='red')


def echo(s):
    click.secho(s)


DEBUG_ON = bool(os.getenv('DEBUG', False))


def debug(s):
    if DEBUG_ON:
        click.secho('[DEBUG] {}'.format(s), fg='green')
