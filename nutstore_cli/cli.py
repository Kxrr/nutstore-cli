# coding: utf-8
from __future__ import absolute_import
import textwrap

import click
from prompt_toolkit import prompt
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import InMemoryHistory

from nutstore_cli import __version__
from nutstore_cli.client.client import NutStoreClient
from nutstore_cli.context import Context
from nutstore_cli.completer import completer
from nutstore_cli.execution import execute
from nutstore_cli.utils import (
    output,
    save_text,
    to_str,
    to_unicode,
)

from nutstore_cli.config import get_config


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


def _launch_cli(client):
    """
    NutStore Command Line Interface (0.4.3)

    NutStore WebDAV Settings: https://github.com/Kxrr/nutstore-cli/blob/master/docs/tutorial.md

    Project Page: https://github.com/Kxrr/nutstore-cli
    """
    output.debug('Client setup done')
    output.info('Hello.'.format(client.username))
    output.info('Type "help" to see supported commands.')
    context = Context(client=client)
    history = InMemoryHistory()
    while True:
        try:
            text = prompt(
                message=u'[{}] > '.format(to_unicode(context.path)),  # message param needs to be unicode
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
    output.info('Goodbye.')


@click.group(help=textwrap.dedent(_launch_cli.__doc__))
@click.pass_context
@click.option(
    '--username',
    prompt='Username',
    default=get_config('username'),
    help='Example: i@example.com',
    cls=NoPromptIfDefaultOption,
)
@click.option(
    '--key',
    prompt='App Key',
    default=get_config('key'),
    help='Example: a2mqieixzkm5t5h4',
    hide_input=True,
    cls=NoPromptIfDefaultOption,

)
@click.option(
    '--working_dir',
    prompt='Working Dir',
    default=get_config('working_dir'),
    help='Example: /photos',
    cls=NoPromptIfDefaultOption,
)
def _main(ctx, username, key, working_dir):
    client = NutStoreClient(username=username, password=key, working_dir=to_str(working_dir), check_conn=False)
    output.debug('Try to initial a client by given args')
    try:
        client.check_conn()
    except Exception as e:
        import traceback
        output.error('Login failed, detail: {0}\n'.format(save_text(traceback.format_exc())))
        import sys
        sys.exit(-1)
    else:
        ctx.obj['client'] = client


@_main.command(help='Launch cli (default)')
@click.pass_context
def interact(ctx):
    _launch_cli(ctx.obj['client'])


@_main.command(help='Upload local file to remote')
@click.pass_context
@click.argument('local_path', required=True)
@click.argument('remote_dir', default=get_config('working_dir'))
def upload(ctx, local_path, remote_dir):
    output.echo(ctx.obj['client'].upload(
        to_str(local_path),
        to_str(remote_dir)
    ))


@_main.command(help='Download remote file to local machine')
@click.pass_context
@click.argument('remote_path', required=True)
@click.argument('local_path', required=False)
def download(ctx, remote_path, local_path):
    output.echo(ctx.obj['client'].download(
        to_str(remote_path),
        to_str(local_path)
    ))


def main():
    output.debug('Current version: {}'.format(__version__))
    import sys
    output.debug('Args: {}'.format(sys.argv))
    if '--help' not in sys.argv and not set(sys.argv) & {'interact', 'upload', 'download'}:
        output.debug('Set "interact" as sub command')
        sys.argv.insert(1, 'interact')
    _main(obj={})


if __name__ == '__main__':
    main()

