# encoding: utf-8
import click
from parsimonious import ParseError
from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

from nutstore_cli.client.exceptions import WebdavException
from nutstore_cli.utils import info

HELP = """

ls: list remote file in working directory
    $ ls 
    $ ls | grep {keyword}

cd: change working directory
    $ cd {absolute_remote_path}
    $ cd {relative_remote_path}

rm:
    $ rm {remote_file_name}

upload: upload local file to remote 
    $ upload {local_file_path}

download: download remote file to a temp local path 
    $ download {remote_file_name}

"""
grammar = Grammar(r"""
    command     = cd / ls / exit / help / download / upload / rm

    rm          = "rm" _ string
    upload      = "upload" _ string
    download    = "download" _ string _ (string)?
    help        = "help" / "h" / "?"
    exit        = "exit" / "quit" / "q"
    ls          = ("ls" / "ll") (grep)?
    cd          = _ "cd" _ string _
    
    grep        = pipe "grep" _ ex_string
    pipe        = _ "|" _

    ex_string   = string / "*" / "-" / "_" / "."
    string      = char+
    char        = ~r"[^\s'\\]"
    _           = ~r"\s*"
""")


class ExecutionVisitor(NodeVisitor):
    unwrapped_exceptions = (WebdavException,)

    def __init__(self, context):
        """
        :type context: nutstore_cli.cli.Context
        """
        super(ExecutionVisitor, self).__init__()

        self.context = context
        self.output = Output()

    def visit_cd(self, node, children):
        path = children[3].text
        self.context.client.cd(path)

    def visit_exit(self, node, children):
        self.context.should_exit = True

    def visit_ls(self, node, children):
        filter_str = children[1].children[3].text if children[1].children else ''
        self.output.write(self.context.client.formatted_ls(filter_str=filter_str))

    def visit_download(self, node, children):
        cloud_path = children[2].text
        store_path = children[4].text if len(node.children) == 5 else None
        self.context.client.download(cloud_path, store_path)

    def visit_upload(self, node, children):
        local_path = children[2].text
        self.context.client.upload(local_path)

    def visit_rm(self, node, children):
        cloud_path = children[2].text
        if click.confirm('rm {}?'.format(cloud_path)):
            self.context.client.rm(cloud_path)

    def visit_help(self, node, children):
        info(HELP)

    def generic_visit(self, node, children):
        if (not node.expr_name) and node.children:
            if len(children) == 1:
                return children[0]
            return children
        return node


class Output(object):
    def write(self, data):
        return click.secho(data, fg='green')


def execute(command, context):
    if not command.strip():
        click.secho('Empty command.'.format(command), fg='red')
        return

    visitor = ExecutionVisitor(context)
    try:
        root = grammar.parse(command)
    except ParseError:
        click.secho('Invalid command <{0}>.'.format(command), fg='red')
        return

    try:
        visitor.visit(root)
    except WebdavException as e:
        click.secho(str(e), fg='red')
