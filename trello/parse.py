from __future__ import annotations

import os
import json
import pprint
import dataclasses
from datetime import datetime
from typing import List, Optional, Generator, Dict, Any
from dataclasses import dataclass


@dataclass
class TrelloLabel:
    id: str
    idBoard: str
    name: str
    color: str


@dataclass
class TrelloList:
    id: str
    name: str
    closed: bool
    idBoard: str
    pos: int
    subscribed: bool


@dataclass
class TrelloCard:
    id: str
    dateLastActivity: datetime
    desc: str
    idBoard: str
    idLabels: str
    idList: str
    name: str
    pos: int
    labels: list
    card_list: TrelloList


TrelloLabels = List[TrelloLabel]
TrelloLists = List[TrelloList]
TrelloCards = List[TrelloCard]

def force_string(thing):
    if isinstance(thing, bytes):
        return thing.encode('utf-8')
    return thing


class TrelloBoard:
    def __init__(
        self,
        labels: TrelloLabels = None,
        lists: TrelloLists = None,
        cards: TrelloCards = None,
    ):
        self._labels = labels or []
        self._lists = lists or []
        self._cards = cards or []

    @property
    def labels(self) -> TrelloLabels:
        return self._labels

    @property
    def lists(self) -> TrelloLists:
        return self._lists

    @property
    def cards(self) -> TrelloCards:
        return self._cards

    def find_label(self, name: str) -> Optional[TrelloLabel]:
        return next((l for l in self.labels if l.name == name), None)

    def find_list(self, list_id: str) -> Optional[TrelloList]:
        return next((l for l in self.lists if l.id == list_id), None)

    def gen_labels(self, label_names: List[str]) -> Generator[TrelloLabel, None, None]:
        for label_name in label_names:
            label = self.find_label(label_name)
            if label:
                yield label

    def get_labels(self, label_names: List[str]) -> TrelloLabels:
        return [label for label in self.gen_labels(label_names)]

    @staticmethod
    def ingest_labels(
        board_data: dict, instance: Optional[TrelloBoard] = None
    ) -> TrelloBoard:
        if not instance:
            instance = TrelloBoard()
        for label in board_data["labels"]:
            instance.labels.append(TrelloLabel(**label))
        return instance

    @staticmethod
    def ingest_lists(
        board_data: dict, instance: Optional[TrelloBoard] = None
    ) -> TrelloBoard:
        if not instance:
            instance = TrelloBoard()
        for l in board_data["lists"]:
            list_args = [i.name for i in dataclasses.fields(TrelloList)]
            list_data = {k: force_string(v) for k, v in l.items() if k in list_args}
            instance.lists.append(TrelloList(**list_data))
        return instance

    @staticmethod
    def ingest_cards(
        board_data: dict, instance: Optional[TrelloBoard] = None
    ) -> TrelloBoard:
        if not instance:
            instance = TrelloBoard()
        for card in board_data["cards"]:
            list_args = [i.name for i in dataclasses.fields(TrelloCard)]
            card_data = {k: force_string(v) for k, v in card.items() if k in list_args}
            card_data["labels"] = instance.get_labels(
                [i["name"] for i in card["labels"]]
            )
            card_data["card_list"] = instance.find_list(card["idList"])
            card_data["dateLastActivity"] = datetime.strptime(
                card_data["dateLastActivity"],
                "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            try:
                _card = TrelloCard(**card_data)
            except Exception as exp:  # noqa F841
                # import pdb; pdb.set_trace()
                continue
            instance.cards.append(_card)
        return instance

    @staticmethod
    def ingest_board_data(board_data: dict) -> TrelloBoard:
        # TODO: make use of reduce here (acc being the instance?)
        instance = TrelloBoard()
        instance = TrelloBoard.ingest_labels(board_data, instance)
        instance = TrelloBoard.ingest_lists(board_data, instance)
        instance = TrelloBoard.ingest_cards(board_data, instance)
        return instance

    def pretty_print(self) -> None:
        print("labels")
        pprint.pprint(self.labels)
        print("\nlists")
        pprint.pprint(self.lists)
        print("\ncards")
        pprint.pprint(self.cards)


def get_trello_data() -> dict:
    trello_data: Dict[str, Any] = {}
    trello_json_path = os.path.join(
        os.path.dirname(__file__),
        "online-reading-2019-07-24.json"
    )
    with open(trello_json_path, "r") as fin:
        trello_data = json.loads(fin.read())
    return trello_data


def get_cards_in_read_list() -> TrelloCards:
    trello_data = get_trello_data()
    trello_instance = TrelloBoard.ingest_board_data(trello_data)
    return [card for card in trello_instance.cards if card.card_list.name == "Read"]


def main() -> None:
    read_cards = get_cards_in_read_list()
    for card in read_cards:
        print(card.name)
        print(card.dateLastActivity)
        print(card.desc)


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
