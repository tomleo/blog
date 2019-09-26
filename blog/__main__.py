#!/usr/bin/env python

"""blog

Usage:
  blog build <src> <dest>
  blog clean <dest>
  blog serve <dest>
  blog (-h | --help)
  blog (-v | --version)

Options:
  -h --help     Show this screen.
  -v --version  Show version.
  --write       Write to disk
"""

import os
import re
import sys
from docopt import docopt

# Not Sure why mypy complains about missing attributes on __main__.blog
# for now ignoring mypy lint errors
from _blog import (  # type: ignore
    serve,
    build,
    clean,
)

COMMAND_BUILD = "build"
COMMAND_CLEAN = "clean"
COMMAND_SERVE = "serve"
SOURCE = "<src>"
DESTINATION = "<dest>"


def get_command(arguments: dict) -> str:
    commands = [COMMAND_SERVE, COMMAND_BUILD, COMMAND_CLEAN]
    return next((k for k, v in arguments.items() if v and k in commands))


VERSION = ''
version_file = os.path.join(
    os.path.abspath(os.path.dirname(__file__)),
    'version.py'
)
with open(version_file, 'r', encoding='utf-8') as fin:
    VERSION = re.sub(r'"', '', fin.read().strip())


if __name__ == "__main__":
    arguments = docopt(__doc__, version=f'blog {VERSION}')
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
    else:
        print(__doc__)
