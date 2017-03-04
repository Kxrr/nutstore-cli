# coding: utf-8
from __future__ import absolute_import

import sys
from os import getenv

import click
from prompt_toolkit import prompt
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory

from nutstore_cli.client import NutStoreClient
from nutstore_cli.context import Context
from nutstore_cli.execution import execute


@click.command()
@click.argument('username', default=getenv('NUTSTORE_USERNAME'))
@click.argument('key', default=getenv('NUTSTORE_KEY'))
@click.argument('working_dir', default=getenv('NUTSTORE_WORKINGDIR'))
def cli(username, key, working_dir):
    click.secho('NutStore Command Line Interface.\n{}\n'.format(sys.version))
    if not all([username, key, working_dir]):
        click.secho('Please login.', fg='cyan')
    if not username:
        username = click.prompt('username')
    if not key:
        key = click.prompt('key', hide_input=True)
    if not working_dir:
        working_dir = click.prompt('working dir')

    # TODO: if retry after login failed(pdb?)
    client = NutStoreClient(username=username, password=key, working_dir=working_dir, check_conn=True)
    context = Context(client=client)
    history = InMemoryHistory()
    while True:
        try:
            text = prompt(
                message=u'[{path}] > '.format(path=context.path),
                history=history,
                auto_suggest=AutoSuggestFromHistory(),
            )
        except EOFError:
            break
        else:
            execute(text, context)
            if context.should_exit:
                break

    click.echo('Goodbye.')
