# coding: utf-8
from __future__ import absolute_import

import os
import click


def info(s):
    click.secho(s, fg='cyan')


def error(s):
    click.secho(s, fg='red')


def echo(s):
    click.secho(s)


_DEBUG = bool(os.getenv('DEBUG', False))


def debug(s):
    if _DEBUG:
        click.secho('[DEBUG] {}'.format(s), fg='green')
