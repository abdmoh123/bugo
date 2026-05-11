from dataclasses import dataclass
from enum import StrEnum
from typing import override


class HTMLTagType(StrEnum):
    A = "a"
    P = "p"
    H = "h"


@dataclass(frozen=True)
class HTMLTag:
    tag_type: HTMLTagType
    level: int | None = None

    @override
    def __str__(self) -> str:
        if (self.level is None):
            return self.tag_type
        return f"{self.tag_type.value}{self.level}"


@dataclass(frozen=True)
class HTMLNode:
    tag: HTMLTag | None = None
    value: str | None = None
    children: list[HTMLNode] | None = None
    props: dict[str, str] | None = None

    @override
    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def to_html(self) -> str:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if (self.props is None):
            return ""

        props_str: str = ""
        for key, value in self.props.items():
            # Leading space is intentional
            props_str += f' {key}="{value}"'
        return props_str


class LeafNode(HTMLNode):
    def __init__(self, tag: HTMLTag | None, value: str, props: dict[str, str] | None = None):
        super().__init__(tag, value, None, props)

    @override
    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

    @override
    def to_html(self) -> str:
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
