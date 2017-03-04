# coding: utf-8
from __future__ import absolute_import

import click
from click import prompt

from cli.context import Context
from cli.execution import execute
from client import NutStoreClient


def cli():
    click.secho('NutStore Command Line Tools.\nWelcome.\n')
    click.secho('Please login.', fg='cyan')
    username = prompt('username')
    password = prompt('key', hide_input=True)
    working_dir = prompt('working dir')
    client = NutStoreClient(username=username, password=password, working_dir=working_dir)
    context = Context(client=client)

    while True:
        try:
            text = prompt('[{cwd}] > '.format(cwd=context.path), prompt_suffix='')
        except EOFError:
            break
        else:
            execute(text, context)
            if context.should_exit:
                break

    click.echo('Goodbye.')
