# coding: utf-8
from nutstore_cli.execution import COMMANDS
from prompt_toolkit.contrib.completers import WordCompleter

completer = WordCompleter(words=COMMANDS, ignore_case=False)
