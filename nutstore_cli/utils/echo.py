# coding: utf-8
from __future__ import absolute_import

import click


def info(s):
    click.secho(s, fg='cyan')


def error(s):
    click.secho(s, fg='red')


def echo(s):
    click.secho(s)
