# coding: utf-8
import click
from prompt_toolkit import prompt

from .context import Context
from .execution import execute
from ..client import NutStoreClient


def cli():
    click.secho('NutStore Command Line Tools.\nWelcome.\n')
    click.secho('Please login.', fg='cyan')
    username = prompt('username: ')
    password = prompt('key: ', is_password=True)
    working_dir = prompt('working dir: ')
    client = NutStoreClient(username=username, password=password, working_dir=working_dir)
    context = Context(client=client)

    while True:
        try:
            text = prompt('[{cwd}] > '.format(cwd=context.path))
        except EOFError:
            break
        else:
            execute(text, context)
            if context.should_exit:
                break

    click.echo('Goodbye.')