from __future__ import annotations

from datetime import datetime
import dataclasses
import pprint
from typing import List, Optional, Generator


@dataclasses.dataclass
class TrelloLabel:
    id: str
    idBoard: str
    name: str
    color: str


TrelloLabels = List[TrelloLabel]


@dataclasses.dataclass
class TrelloList:
    id: str
    name: str
    closed: bool
    idBoard: str
    pos: int
    subscribed: bool


TrelloLists = List[TrelloList]


@dataclasses.dataclass
class TrelloCard:
    id: str
    dateLastActivity: datetime
    desc: str
    idBoard: str
    idLabels: str
    idList: str
    name: str
    pos: int
    labels: Optional[TrelloLabels]
    card_list: TrelloList


TrelloCards = List[TrelloCard]


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

    @staticmethod
    def _gen_filter_labels(label_names: List[str], labels: TrelloLabels) -> Generator[TrelloLabel, None, None]:
        for label_obj in labels:
            if label_obj.name in label_names:
                yield label_obj

    @staticmethod
    def filter_labels(label_names: List[str], labels: TrelloLabels) -> Optional[TrelloLabels]:
        return [label_obj for label_obj in TrelloBoard._gen_filter_labels(label_names, labels)]

    def pretty_print(self) -> None:
        print("labels")
        pprint.pprint(self.labels)
        print("\nlists")
        pprint.pprint(self.lists)
        print("\ncards")
        pprint.pprint(self.cards)
