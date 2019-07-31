import sys

# Not Sure why mypy complains about missing attributes on __main__.blog
# for now ignoring mypy lint errors
from blog import (  # type: ignore
    serve,
    build,
    clean,
    trello_json_export_to_markdown_files,
)

USAGE = """
./blog.py COMMAND

COMMAND:
    serve               run HTTP server for local testing
    build               compile to static HTML in build/ directory
    clean               remove compiled files
    trello              parse .json trello dump, convert into markdown files
"""

TRELLO_USAGE = """
./blog.py trello <file-name> <trello-list>
"""

if __name__ == "__main__":
    COMMAND_SERVE = "serve"
    COMMAND_BUILD = "build"
    COMMAND_CLEAN = "clean"
    COMMAND_TRELLO = "trello"
    commands = {
        COMMAND_SERVE: serve,
        COMMAND_BUILD: build,
        COMMAND_CLEAN: clean,
        COMMAND_TRELLO: trello_json_export_to_markdown_files,
    }

    try:
        command = sys.argv[1]
    except IndexError:
        print(USAGE)
        sys.exit()
    except Exception as exp:
        print(exp)
        sys.exit(1)
    if command not in commands:
        print(USAGE)
        sys.exit()
    if command == COMMAND_TRELLO:
        try:
            trello_file = sys.argv[2]
            trello_list_name = sys.argv[3]
        except Exception as exp:
            print(exp)
            print(TRELLO_USAGE)
            sys.exit(1)
        else:
            trello_json_export_to_markdown_files(
                trello_file,
                trello_list_name,
            )
            sys.exit()
    commands[command]()  # type: ignore
