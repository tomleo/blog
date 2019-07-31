import os
import re
import yaml
import http.server
import socketserver
from datetime import datetime
from typing import Generator
import markdown

from trello.view import (
    get_trello_board_dict_from_json,
    get_cards_in_list,
)
from trello.model import (
    TrelloCard,
)
from utils import (
    mkdirp,
    slugify,
)
from meta_files.model import (
    FileContext,
    FileContextBody,
    FileContextMeta,
    Md,
)
from jinja2 import (
    Environment,
    PackageLoader,
    # select_autoescape,
)

env = Environment(
    loader=PackageLoader("theme", "templates"),
    # autoescape=select_autoescape(['html'])
)


default_markdown_parser = markdown.Markdown(
    extensions=[
            'markdown.extensions.tables',
            'markdown.extensions.admonition',
            'markdown.extensions.smarty',
            'pymdownx.magiclink',
            'pymdownx.betterem',
            'pymdownx.tilde',
            'pymdownx.emoji',
            'pymdownx.tasklist',
            'pymdownx.superfences',
            'pymdownx.highlight',
            'pyembed.markdown',  # https://pyembed.github.io/usage/markdown/
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
    return Md('', markdown_text)


def extract_meta_from_markdown_text(markdown_text: str, meta_parser=yaml.safe_load) -> dict:
    return meta_parser(split_meta_from_markdown(markdown_text).yaml_meta)


def generate_html_from_markdown_content(markdown_text: str, markdown_parser=default_markdown_parser) -> str:
    return markdown_parser.convert(
        split_meta_from_markdown(markdown_text).markdown_content
    )


def parse_markdown_file(file_path, encoding="utf-8") -> FileContext:
    with open(file_path, "rb") as fin:
        markdown_text = fin.read().decode(encoding)

        context_meta = FileContextMeta(
            extract_meta_from_markdown_text(markdown_text)
        )
        context_body = FileContextBody(
            generate_html_from_markdown_content(markdown_text)
        )
        return FileContext(meta=context_meta, content=context_body)


def file_context_to_html(context: FileContext) -> str:
    template = env.get_template(context.get_template())
    return template.render(context.get_context())


def generate_html_from_markdown_file(file_path: str) -> None:
    file_context = parse_markdown_file(file_path)
    if not file_context.content.content:
        return
    html_content = file_context_to_html(file_context)
    rel_path = re.sub(r"\.\/?content\/", "", os.path.dirname(file_path))
    rel_name = re.sub(r"\.md$", ".html", os.path.basename(file_path))
    build_dir = os.path.join("./build", rel_path)
    mkdirp(build_dir)
    build_path = os.path.join(build_dir, rel_name)
    with open(build_path, "wb") as fout:
        fout.write(html_content.encode("utf-8"))


def generate_html_from_markdown_directory(markdown_directory: str = "./content") -> None:
    for file_path in traverse_files_in_path(markdown_directory):
        generate_html_from_markdown_file(file_path)


def create_markdown_file_from_trello_card(card: TrelloCard) -> None:
    labels = card.labels or []
    if labels:
        card_folder_name = slugify(labels[0].name)
    else:
        card_folder_name = "unclassified"
    card_folder_path = os.path.join(
        os.path.dirname(__file__),
        'content',
        'trello',
        card_folder_name,
        datetime.strftime(card.dateLastActivity, "%Y-%m-%d"),
    )
    mkdirp(card_folder_path)
    # TODO: add lastmodified, labels, ect.
    markdown_meta = yaml.dump({
        'title': card.name,
    })
    markdown_content = "---\n{}\n---\n{}".format(markdown_meta, card.desc)
    markdown_file_name = "{}.md".format(slugify(card.name))
    markdown_file_path = os.path.join(card_folder_path, markdown_file_name)
    with open(markdown_file_path, 'wb') as fout:
        fout.write(markdown_content.encode('utf-8'))


def trello_json_export_to_markdown_files(trello_file: str, trello_list_name: str, write_to_disk: bool = True):
    """
    Reads trello board JSON export, and converts card into markdown files
    """

    trello_file_path = os.path.abspath(trello_file)
    trello_data = get_trello_board_dict_from_json(trello_file_path)
    read_cards = get_cards_in_list(trello_data, trello_list_name)
    if write_to_disk:
        for card in read_cards:
            create_markdown_file_from_trello_card(card)


def build() -> None:
    generate_html_from_markdown_directory()


def serve() -> None:
    LOCALHOST = "127.0.0.1"
    PORT = int(os.environ.get("BLOG_PORT", 8000))
    web_dir = os.path.join(os.path.dirname(__file__), "build")
    os.chdir(web_dir)
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("127.0.0.1", PORT), Handler)
    print(f"serving http://{LOCALHOST}:{PORT}")
    httpd.serve_forever()


def clean() -> None:
    for root, dirs, files in os.walk("./build"):
        if files:
            for file in files:
                file_path = os.path.join(root, file)
                if file_path.endswith('.keep'):
                    continue
                os.remove(file_path)
        try:
            os.removedirs(root)
        except OSError:
            pass
