# coding: utf-8
import tabulate

help_rows = []
help_labels = ('Command', 'Description', 'Examples')


def add_help(command, description, examples=None):
    examples = examples or ['']
    for idx, example in enumerate(examples):
        if idx == 0:
            help_rows.append(
                [command, description, example]
            )
        else:
            help_rows.append(
                ['', '', example]
            )


add_help(
    'cd',
    'change working directory',
    ['cd {absolute_remote_path}', 'cd {remote_path}']
)

add_help(
    'download',
    'download a remote file to the local temp path ',
    ['download {remote_file_name}'],
)

add_help(
    'exit',
    'exit from the interface',
    ['exit']
)

add_help(
    'help',
    'show help',
    ['help']
)

add_help(
    'ls',
    'list remote files in working directory',
    ['ls', 'ls | grep {keyword}']
)

add_help(
    'rm',
    'delete a remote file',
    ['rm {remote_file_name}']
)

add_help(
    'upload',
    'upload a local file to remote ',
    ['upload {local_file_path}']
)

help_table = tabulate.tabulate(
    help_rows,
    headers=help_labels,
    tablefmt='grid',
)
