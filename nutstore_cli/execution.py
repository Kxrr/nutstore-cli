# encoding: utf-8
import re
from os import path
from itertools import ifilter

import click
import tabulate
from dateutil.parser import parse as dt_parse
from dateutil import tz
from parsimonious import ParseError
from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

from nutstore_cli.utils import echo, humanbytes
from nutstore_cli.command_help import help_table
from nutstore_cli.client.exceptions import WebdavException

COMMANDS = ['cd', 'download', 'exit', 'grep', 'help', 'ls', 'll', 'rm', 'upload']

RULES = r"""
    command     = cd / ls / exit / help / download / upload / rm

    rm          = "rm" _ string
    upload      = "upload" _ string
    download    = "download" _ string _ (string)?
    help        = "help" / "h" / "?"
    exit        = "exit" / "quit" / "q"
    ls          = ("ls" / "ll") _ (grep)?
    cd          = _ "cd" _ string _
    
    grep        = pipe _ "grep" _ ex_string
    
    pipe        = "|"

    ex_string   = string / "*" / "-" / "_" / "."
    string      = char+
    char        = ~r"[^\s'\\]"
    _           = ~r"\s*"
"""

grammar = Grammar(RULES)

LS_ATTRS = (
    lambda f: path.basename(f.name),
    lambda f: humanbytes(int(f.size)),
    lambda f: dt_parse(f.mtime).astimezone(tz.tzlocal()).strftime('%Y-%m-%d %H:%M:%S')
)

LS_LABELS = ('Filename', 'Size', 'Modify Time')


class ExecutionVisitor(NodeVisitor):
    unwrapped_exceptions = (WebdavException,)

    def __init__(self, context):
        """
        :type context: nutstore_cli.cli.Context
        """
        super(ExecutionVisitor, self).__init__()

        self.context = context

    def visit_cd(self, node, children):
        path = children[3].text
        self.context.client.cd(path)

    def visit_exit(self, node, children):
        self.context.should_exit = True

    def visit_ls(self, node, children):
        labels, rows = self.context.client.list(
            LS_ATTRS,
            LS_LABELS
        )
        grep_keywords = children[2].children[4].children[0].text if children[2].children else None
        rows = ifilter(lambda row: bool(row[0]), rows)
        if grep_keywords:
            echo.debug('Issue a grep "{}"'.format(grep_keywords))
            rows = ifilter(lambda row: re.search(grep_keywords, row[0], flags=re.IGNORECASE), rows)
        rows = list(rows)
        rows.sort(key=lambda row: row[2])  # order by mtime
        echo.echo(tabulate.tabulate(rows, headers=labels))

    def visit_download(self, node, children):
        cloud_path = children[2].text
        store_path = children[4].text if len(node.children) == 5 else None
        dest = self.context.client.download(cloud_path, store_path)
        echo.echo(dest)

    def visit_upload(self, node, children):
        local_path = children[2].text
        remote_path = self.context.client.upload(local_path)
        echo.echo(remote_path)

    def visit_rm(self, node, children):
        cloud_path = children[2].text
        if click.confirm('rm {}?'.format(cloud_path)):
            self.context.client.rm(cloud_path)

    def visit_help(self, node, children):
        echo.info(help_table)

    def generic_visit(self, node, children):
        if (not node.expr_name) and node.children:
            if len(children) == 1:
                return children[0]
            return children
        return node


def execute(command, context):
    if not command.strip():
        return

    visitor = ExecutionVisitor(context)
    try:
        root = grammar.parse(command)
    except ParseError:
        echo.error('Invalid command "{0}".'.format(command))
        echo.info('Type "help" to see supported commands.')
        return

    try:
        visitor.visit(root)
    except WebdavException as e:
        echo.error(str(e))
