import os
import dataclasses
from typing import NamedTuple


class FileContextMeta:
    TEMPLATE_STR = "template"
    DEFAULT_TEMPLATE_STR = "default"

    def __init__(self, meta: dict = None):
        if not meta:
            meta = {}
        self._template = meta.get(self.TEMPLATE_STR, self.DEFAULT_TEMPLATE_STR)
        self._meta = {k: v for k, v in meta.items() if k != self.TEMPLATE_STR}

    @property
    def template(self) -> str:
        return self._template

    def items(self):
        yield (self.TEMPLATE_STR, self.template)
        for k, v in self._meta.items():
            yield (k, v)

    def __getitem__(self, key):
        if key == self.TEMPLATE_STR:
            return self.template
        return self._meta[key]

    def __setitem__(self, key, val):
        if key == self.TEMPLATE_STR:
            self._template = val
        else:
            self._meta[key] = val

    def as_dict(self) -> dict:
        return {k: v for (k, v) in self.items()}


@dataclasses.dataclass
class FileContextBody:
    content: str


@dataclasses.dataclass
class FileContext:
    meta: FileContextMeta
    content: FileContextBody

    def get_template(self) -> str:
        return f"{self.meta.template}.html"

    def get_context(self) -> dict:
        return {
            "meta": self.meta.as_dict(),
            "content": self.content.content
        }


class Md(NamedTuple):
    yaml_meta: str
    markdown_content: str


@dataclasses.dataclass
class DestFile:
    """
    Keep track of filename and folder
    """
    dest_file_name: str
    dest_file_folder: str

    @property
    def dest_file_path(self) -> str:
        return os.path.join(
            self.dest_file_folder,
            self.dest_file_name
        )


class FolderMeta(NamedTuple):
    dir_path: str
    files: str
    has_dirs: str  # TODO: should this be a bool?
