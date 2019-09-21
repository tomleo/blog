from __future__ import annotations

from datetime import datetime
from typing import Any

from .model import (
    TrelloBoard, TrelloLabel, TrelloLabels, TrelloList, TrelloLists, TrelloCard, TrelloCards
)


def _force_string(thing: Any) -> str:
    if isinstance(thing, bytes):
        return thing.encode('utf-8')  # type: ignore
    return thing


def ingest_label(label_data: dict) -> TrelloLabel:
    return TrelloLabel(**label_data)


def ingest_labels(board_data: dict) -> TrelloLabels:
    return [ingest_label(label_data) for label_data in board_data["labels"]]


def ingest_list(list_data: dict) -> TrelloList:
    return TrelloList(
        id=list_data['id'],
        name=list_data['name'],
        closed=list_data['closed'],
        idBoard=list_data['idBoard'],
        pos=list_data['pos'],
        subscribed=list_data['subscribed'])


def ingest_lists(board_data: dict) -> TrelloLists:
    return [ingest_list(list_data) for list_data in board_data["lists"]]


def ingest_card(card_data: dict, lists: TrelloLists, labels: TrelloLabels = None) -> TrelloCard:
    card_list = next((l for l in lists if l.id == card_data['idList']))
    return TrelloCard(
        id=card_data['id'],
        dateLastActivity=datetime.strptime(
            card_data["dateLastActivity"],
            "%Y-%m-%dT%H:%M:%S.%fZ",
        ),
        desc=card_data['desc'],
        idBoard=card_data['idBoard'],
        idLabels=card_data['idLabels'],
        idList=card_data['idList'],
        name=card_data['name'],
        pos=card_data['pos'],
        labels=labels,
        card_list=card_list,
    )


def ingest_cards(
    board_data: dict, lists: TrelloLists, labels: TrelloLabels = None
) -> TrelloCards:
    return ([ingest_card(card_data, lists, labels) for card_data in board_data["cards"]])


def ingest_board_data(board_data: dict) -> TrelloBoard:
    labels = ingest_labels(board_data)
    lists = ingest_lists(board_data)
    cards = ingest_cards(board_data, lists, labels)
    return TrelloBoard(
        labels=labels,
        lists=lists,
        cards=cards,
    )
