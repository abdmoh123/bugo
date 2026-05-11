from dataclasses import dataclass
from enum import StrEnum, auto
from typing import override


class TextType(StrEnum):
    TEXT = auto()
    BOLD = auto()
    ITALIC = auto()
    CODE = auto()
    LINK = auto()
    IMAGE = auto()


@dataclass()
class TextNode:
    text: str
    text_type: TextType
    url: str | None = None

    @override
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
