# encoding: utf-8
import re
from collections import OrderedDict
from os import path
from itertools import ifilter
from urllib import unquote

import click
import tabulate
from dateutil.parser import parse as dt_parse
from dateutil import tz
from parsimonious import ParseError
from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

from nutstore_cli.utils import output, humanbytes, to_str
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


class PrettyFile(object):
    def __init__(self, efile):
        """
        :type efile: easywebdav.client.File
        """
        self._file = efile
        self._name = unquote(path.basename(efile.name)).decode('utf-8')

        self.is_dir = efile.contenttype == 'httpd/unix-directory'
        self.name = self._name
        self.size = humanbytes(int(efile.size))
        self.modify_time = dt_parse(efile.mtime).astimezone(tz.tzlocal()).strftime('%Y-%m-%d %H:%M:%S')
        if self.is_dir:
            self.name = click.style(self._name, fg='cyan')
            self.size = ''

    def pack(self):
        return self.name, self.size, self.modify_time


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
        self.context.client.cd(to_str(path))

    def visit_exit(self, node, children):
        self.context.should_exit = True

    def visit_ls(self, node, children):
        pretty_files = [PrettyFile(ef) for ef in self.context.client.ls()]
        grep_keywords = children[2].children[4].children[0].text if children[2].children else None
        if grep_keywords:
            output.debug('Issue a grep "{}"'.format(grep_keywords))
            pretty_files = ifilter(lambda pfile: re.search(grep_keywords, pfile._name, flags=re.IGNORECASE),
                                   pretty_files)
        pretty_files = ifilter(lambda pfile: bool(pfile._name), pretty_files)  # ignore who has a empty filename
        pretty_files = sorted(pretty_files, key=lambda pfile: pfile.modify_time)
        output.echo(tabulate.tabulate(
            [pfile.pack() for pfile in pretty_files],
            headers=['Filename', 'Size', 'Modify Time']
        ))

    def visit_download(self, node, children):
        cloud_path = children[2].text
        store_path = children[4].text if len(node.children) == 5 else None
        dest = self.context.client.download(to_str(cloud_path), to_str(store_path))
        output.echo(dest)

    def visit_upload(self, node, children):
        local_path = to_str(children[2].text)
        remote_path = self.context.client.upload(local_path)
        output.echo(remote_path)

    def visit_rm(self, node, children):
        cloud_path = to_str(children[2].text)
        if click.confirm('rm {}?'.format(cloud_path)):
            self.context.client.rm(cloud_path)

    def visit_help(self, node, children):
        output.info(help_table)

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
        output.error('Invalid command "{0}".'.format(command))
        output.info('Type "help" to see supported commands.')
        return

    try:
        visitor.visit(root)
    except WebdavException as e:
        output.error(str(e))
