from __future__ import annotations

import os
import json

from typing import Dict, Any

from .model import (
    TrelloCards
)
from .controller import (
    ingest_board_data,
)


def get_trello_board_dict_from_json(trello_file_path: str) -> dict:
    trello_data: Dict[str, Any] = {}
    trello_json_path = os.path.join(
        os.path.dirname(__file__),
        "json_data",
        trello_file_path
    )
    with open(trello_json_path, "r") as fin:
        trello_data = json.loads(fin.read())
    return trello_data


def get_cards_in_list(trello_data: dict, list_name: str) -> TrelloCards:
    trello_instance = ingest_board_data(trello_data)
    return [card for card in trello_instance.cards if card.card_list.name == list_name]


"""
Likely Ingestion Process:

1. JSON -> TrelloBoard
2. TrelloBoard.cards -> .md + .md5 checksum of desc
3. .md -> .html

During Re-ingestion:
- If .md file exists
- generate and compare .md5 files
- If .md5 files differ, generate new .md + .md5 file
- Else do nothing

Possible Enhancement:

content
YYYY-MM-DD/
    file1.md
    file2.md
    file1.html.checksum
    file2.html.checksum

Generate HTML file in memory
Generate Checksum in memory
Compare checksum against existing one,
    if no existing checksum or they differ
        generate HTML file
        generate checksum file
"""
