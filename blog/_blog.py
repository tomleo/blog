import os
import re
import yaml
import http.server
import socketserver
from typing import Generator, List
from shutil import copyfile

import markdown
import logging
from jinja2 import Environment, FileSystemLoader

from utils import mkdirp
from meta_files.model import (
    FileContext,
    FileContextBody,
    FileContextMeta,
    Md,
    DestFile,
    FolderMeta,
)

template_path = os.path.join(
    os.path.dirname(__file__),
    'theme',
    'templates',
)
template_loader = FileSystemLoader([template_path])

env = Environment(loader=template_loader)
# autoescape=select_autoescape(['html'])


logger = logging.getLogger('basicLogger')
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(
    logging.Formatter('%(message)s')
)
logger.addHandler(console_handler)

default_markdown_parser = markdown.Markdown(
    extensions=[
        "markdown.extensions.tables",
        "markdown.extensions.admonition",
        "markdown.extensions.smarty",
        "pymdownx.magiclink",
        "pymdownx.betterem",
        "pymdownx.tilde",
        "pymdownx.emoji",
        "pymdownx.tasklist",
        "pymdownx.superfences",
        "pymdownx.highlight",
        "pyembed.markdown",  # https://pyembed.github.io/usage/markdown/
    ],
    extension_configs={},
)


def traverse_files_in_path(folder_path) -> Generator[str, None, None]:
    for root, dirs, files in os.walk(folder_path):
        if not files:
            continue
        for file in files:
            yield os.path.join(root, file)


def split_meta_from_markdown(markdown_text) -> Md:
    if markdown_text.startswith("---"):
        try:
            return Md(*markdown_text.split("---")[1:3])
        except IndexError:
            pass
    return Md("", markdown_text)


def extract_meta_from_markdown_text(
    markdown_text: str, meta_parser=yaml.safe_load
) -> dict:
    return meta_parser(split_meta_from_markdown(markdown_text).yaml_meta)


def generate_html_from_markdown_content(
    markdown_text: str, markdown_parser=default_markdown_parser
) -> str:
    return markdown_parser.convert(
        split_meta_from_markdown(markdown_text).markdown_content
    )


def parse_markdown_file(file_path, encoding="utf-8") -> FileContext:
    with open(file_path, "rb") as fin:
        markdown_text = fin.read().decode(encoding)

        context_meta = FileContextMeta(extract_meta_from_markdown_text(markdown_text))
        context_body = FileContextBody(
            generate_html_from_markdown_content(markdown_text)
        )
        return FileContext(meta=context_meta, content=context_body)


def file_context_to_html(context: FileContext) -> str:
    template = env.get_template(context.get_template())
    return template.render(context.get_context())


def get_full_dest_file_path(file_path: str, source_dir: str, dest_dir: str) -> DestFile:
    relative_folder_path = os.path.dirname(file_path)[len(source_dir):]
    if relative_folder_path:
        if relative_folder_path.startswith('/'):
            relative_folder_path = relative_folder_path[1:]
        if relative_folder_path[-1] != '/':
            relative_folder_path = relative_folder_path + '/'

    output_file_name = os.path.basename(file_path)
    if os.path.splitext(file_path)[1] == '.md':
        output_file_name = re.sub(r"\.md$", ".html", output_file_name)
    output_file_folder = os.path.join(dest_dir, relative_folder_path)
    return DestFile(
        dest_file_name=output_file_name,
        dest_file_folder=output_file_folder
    )


def generate_html_from_markdown_file(
    file_path: str, source_dir: str, dest_dir: str
) -> str:
    file_context = parse_markdown_file(file_path)
    if not file_context.content.content:
        raise Exception("Markdown file missing content")
    html_content = file_context_to_html(file_context)
    return html_content


def build(src_dir: str, dest_dir: str) -> None:
    for file_path in traverse_files_in_path(src_dir):
        extension = os.path.splitext(file_path)[1]
        html_content = None
        dest_file = get_full_dest_file_path(file_path, src_dir, dest_dir)
        if extension == '.md':
            try:
                html_content = generate_html_from_markdown_file(file_path, src_dir, dest_dir)
            except Exception as exp:
                print(f"{file_path} {str(exp)}")
                continue

        mkdirp(dest_file.dest_file_folder)
        if html_content:
            with open(dest_file.dest_file_path, "wb") as fout:
                fout.write(html_content.encode("utf-8"))
        else:
            copyfile(file_path, dest_file.dest_file_path)


def serve(dest_dir: str) -> None:
    LOCALHOST = "127.0.0.1"
    PORT = int(os.environ.get("BLOG_PORT", 8000))
    web_dir = os.path.join(os.path.dirname(__file__), dest_dir)
    os.chdir(web_dir)
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), Handler)
    print(f"serving http://{LOCALHOST}:{PORT}")
    httpd.serve_forever()


def _get_tail_nodes_in_folder(dest_dir) -> List[FolderMeta]:
    """
    Traverse through a folder and return only FolderMeta
    of files without child folders
    """
    folders = []
    for root, dirs, files in os.walk(dest_dir):
        folders.append(
            FolderMeta(
                dir_path=root,
                files=[os.path.join(root, file) for file in files],
                has_dirs=bool(len(dirs))))
    return [i for i in folders if not i.has_dirs]


def clean(dest_dir: str) -> None:
    """
    1. Traverse through folder finding folders without child folders
    2. Delete "tail" folders and their files
    3. Repeat until all "child" folders of "dest_dir" are deleted

    If _get_tail_nodes_in_folder is called 100 times print error message
    """
    for i in range(100):
        folders_to_delete = _get_tail_nodes_in_folder(dest_dir)
        if not folders_to_delete:
            return
        for folder in folders_to_delete:
            if folder.dir_path == dest_dir:
                return
            for file in folder.files:
                if ".keep" in file:
                    continue
                os.remove(file)
            if ".keep" not in [os.path.basename(f) for f in folder.files]:
                os.removedirs(folder.dir_path)
    else:
        raise Exception("Too many sub-folder levels")
