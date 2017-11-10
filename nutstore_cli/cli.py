# coding: utf-8
from __future__ import absolute_import
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


class DefaultGroup(click.Group):
    """ https://github.com/pallets/click/issues/430 """

    ignore_unknown_options = True

    def __init__(self, *args, **kwargs):
        default_command = kwargs.pop('default_command', None)
        super(DefaultGroup, self).__init__(*args, **kwargs)
        self.default_cmd_name = None
        if default_command is not None:
            self.set_default_command(default_command)

    def set_default_command(self, command):
        if isinstance(command, basestring):
            cmd_name = command
        else:
            cmd_name = command.name
            self.add_command(command)
        self.default_cmd_name = cmd_name

    def parse_args(self, ctx, args):
        if not args and self.default_cmd_name is not None:
            args.insert(0, self.default_cmd_name)
        return super(DefaultGroup, self).parse_args(ctx, args)

    def get_command(self, ctx, cmd_name):
        if cmd_name not in self.commands and self.default_cmd_name is not None:
            ctx.args0 = cmd_name
            cmd_name = self.default_cmd_name
        return super(DefaultGroup, self).get_command(ctx, cmd_name)

    def resolve_command(self, ctx, args):
        cmd_name, cmd, args = super(DefaultGroup, self).resolve_command(ctx, args)
        args0 = getattr(ctx, 'args0', None)
        if args0 is not None:
            args.insert(0, args0)
        return cmd_name, cmd, args


def _launch_cli(client):
    """
    NutStore Command Line Interface (0.4.0)

    NutStore WebDAV Settings: https://github.com/Kxrr/nutstore-cli/blob/master/docs/tutorial.md

    Project Page: https://github.com/Kxrr/nutstore-cli
    """
    echo.debug('Client setup done')
    echo.info('Hello.'.format(client.username))
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


@click.group(cls=DefaultGroup, help=textwrap.dedent(_launch_cli.__doc__), default_command='launch_cli')
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
def cli(ctx, username, key, working_dir):
    client = NutStoreClient(username=username, password=key, working_dir=working_dir, check_conn=False)
    echo.debug('Try to initial a client by given args')
    try:
        client.check_conn()
    except Exception as e:
        import traceback
        echo.error('Login failed, detail: {0}\n').format(to_file(traceback.format_exc()))
        import sys
        sys.exit(-1)
    else:
        ctx.obj['client'] = client


@cli.command(help='Launch cli (default command)')
@click.pass_context
def launch_cli(ctx):
    _launch_cli(ctx.obj['client'])


@cli.command(help='Upload local file to remote')
@click.pass_context
@click.argument('local_path', required=True)
@click.argument('remote_dir', default=get_config('working_dir'))
def upload(ctx, local_path, remote_dir):
    echo.echo(ctx.obj['client'].upload(local_path, remote_dir))


@cli.command(help='Download remote file to local machine')
@click.pass_context
@click.argument('remote_path', required=True)
@click.argument('local_path', required=False)
def download(ctx, remote_path, local_path):
    echo.echo(ctx.obj['client'].download(remote_path, local_path))


if __name__ == '__main__':
    cli(obj={})
