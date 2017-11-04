# coding: utf-8
from __future__ import absolute_import

import os
import click
import textwrap
from prompt_toolkit import prompt
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory

from nutstore_cli.client.client import NutStoreClient
from nutstore_cli.context import Context
from nutstore_cli.completer import completer
from nutstore_cli.execution import execute
from nutstore_cli.utils import to_file, echo


def cli(username, key, working_dir):
    """
    NutStore Command Line Interface (0.3.4)

    NutStore WebDAV Settings: https://github.com/Kxrr/nutstore-cli/blob/master/docs/tutorial.md

    Project Page: https://github.com/Kxrr/nutstore-cli
    """
    client = NutStoreClient(username=username, password=key, working_dir=working_dir, check_conn=False)
    try:
        client.check_conn()
    except Exception as e:
        import traceback
        echo.error('Login failed, detail: {0}\n'
                   'Usage: nutstore-cli --help'.format(to_file(traceback.format_exc())))
        import sys
        sys.exit(-1)
    echo.info('Hello.'.format(username))
    echo.info('Type "help" to see supported commands.')
    context = Context(client=client)
    history = InMemoryHistory()
    while True:
        try:
            text = prompt(
                message=u'[{path}] > '.format(path=context.path),
                completer=completer,
                history=history,
                auto_suggest=AutoSuggestFromHistory(),
            )
        except EOFError:
            break
        else:
            execute(text, context)
            if context.should_exit:
                break
    echo.info('Goodbye.')


def get_env(key, prefix='NUTSTORE_'):
    def wrapper(*args, **kwargs):
        return os.environ.get('{0}{1}'.format(prefix, key.upper()), '')

    return wrapper


class NoPromptIfDefaultOption(click.Option):
    def prompt_for_value(self, ctx):
        default = self.get_default(ctx)
        if default:
            return default
        if self.is_bool_flag:
            return click.confirm(self.prompt)
        return click.prompt(
            self.prompt,
            hide_input=self.hide_input,
            confirmation_prompt=self.confirmation_prompt,
            value_proc=lambda x: self.process_value(ctx, x)
        )


@click.command(help=textwrap.dedent(cli.__doc__))
@click.option(
    '--username',
    prompt='Username',
    default=get_env('USERNAME'),
    help='Example: i@example.com',
    cls=NoPromptIfDefaultOption,
)
@click.option(
    '--key',
    prompt='App Key',
    default=get_env('KEY'),
    help='Example: a2mqieixzkm5t5h4',
    hide_input=True,
    cls=NoPromptIfDefaultOption,

)
@click.option(
    '--working_dir',
    prompt='Working Dir',
    default=get_env('WORKING_DIR'),
    help='Example: /photos',
    cls=NoPromptIfDefaultOption,
)
def launch_cli(*args, **kwargs):
    return cli(*args, **kwargs)


if __name__ == '__main__':
    launch_cli()
