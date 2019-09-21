#!/usr/bin/env python

"""pystatic

Usage:
  pystatic build <src> <dest>
  pystatic clean <dest>
  pystatic serve <dest>
  pystatic trello <json_file> <list_name> [--write]
  pystatic (-h | --help)
  pystatic (-v | --version)

Options:
  -h --help     Show this screen.
  -v --version  Show version.
  --write       Write to disk
"""

import os
import sys
from docopt import docopt

# Not Sure why mypy complains about missing attributes on __main__.blog
# for now ignoring mypy lint errors
from ._blog import (  # type: ignore
    serve,
    build,
    clean,
)
from .trello_to_markdown import (
    trello_json_export_to_markdown_files,
)

COMMAND_BUILD = "build"
COMMAND_CLEAN = "clean"
COMMAND_SERVE = "serve"
COMMAND_TRELLO = "trello"
SOURCE = "<src>"
DESTINATION = "<dest>"


def get_command(arguments: dict) -> str:
    commands = [COMMAND_SERVE, COMMAND_BUILD, COMMAND_CLEAN, COMMAND_TRELLO]
    return next((k for k, v in arguments.items() if v and k in commands))


if __name__ == "__main__":
    arguments = docopt(__doc__, version='pystatic 1.0')
    command = get_command(arguments)
    if command == COMMAND_BUILD:
        src_dir = os.path.abspath(arguments[SOURCE])
        dest_dir = os.path.abspath(arguments[DESTINATION])
        build(src_dir=src_dir, dest_dir=dest_dir)
    elif command == COMMAND_CLEAN:
        dest_dir = os.path.abspath(arguments[DESTINATION])
        try:
            clean(dest_dir=dest_dir)
        except Exception as exp:
            sys.stderr.write(str(exp))
    elif command == COMMAND_SERVE:
        dest_dir = os.path.abspath(arguments[DESTINATION])
        serve(dest_dir=dest_dir)
    elif command == COMMAND_TRELLO:
        trello_file = os.path.abspath(arguments['json_file'])
        trello_json_export_to_markdown_files(
            trello_file=trello_file,
            trello_list_name=arguments['list_name'],
            write_to_disk=arguments['write'])
    else:
        print(__doc__)
