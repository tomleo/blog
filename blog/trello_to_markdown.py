import os
import yaml
from datetime import datetime

from trello.view import get_trello_board_dict_from_json, get_cards_in_list
from trello.model import TrelloCard
from utils import mkdirp, slugify


def create_markdown_file_from_trello_card(
    card: TrelloCard, trello_folder_name: str = "content/trello"
) -> None:
    labels = card.labels or []
    if labels:
        card_folder_name = slugify(labels[0].name)
    else:
        card_folder_name = "unclassified"
    card_folder_path = os.path.join(
        os.path.dirname(__file__),
        trello_folder_name,
        card_folder_name,
        datetime.strftime(card.dateLastActivity, "%Y-%m-%d"),
    )
    mkdirp(card_folder_path)
    # TODO: add lastmodified, labels, ect.
    markdown_meta = yaml.dump({"title": card.name})
    markdown_content = "---\n{}\n---\n{}".format(markdown_meta, card.desc)
    markdown_file_name = "{}.md".format(slugify(card.name))
    markdown_file_path = os.path.join(card_folder_path, markdown_file_name)
    with open(markdown_file_path, "wb") as fout:
        fout.write(markdown_content.encode("utf-8"))


def trello_json_export_to_markdown_files(
    trello_file: str, trello_list_name: str, write_to_disk: bool = True
):
    """
    Reads trello board JSON export, and converts card into markdown files
    """

    trello_file_path = os.path.abspath(trello_file)
    trello_data = get_trello_board_dict_from_json(trello_file_path)
    read_cards = get_cards_in_list(trello_data, trello_list_name)
    if write_to_disk:
        for card in read_cards:
            create_markdown_file_from_trello_card(card)
