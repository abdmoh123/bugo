from dataclasses import dataclass
from enum import StrEnum, auto
import re
from typing import override

from src.md_utils import extract_markdown_images, extract_markdown_links


class TextType(StrEnum):
    TEXT = auto()
    BOLD = auto()
    ITALIC = auto()
    CODE = auto()
    LINK = auto()
    IMAGE = auto()


def get_delimiters(text_type: TextType) -> list[str]:
    match (text_type):
        case TextType.TEXT:
            return []
        case TextType.BOLD:
            return ["**"]
        case TextType.ITALIC:
            return ["*", "_"]
        case TextType.CODE:
            return ["`"]
        case _:
            raise NotImplementedError(f"{text_type} not implemented")


@dataclass()
class TextNode:
    text: str
    text_type: TextType
    url: str | None = None

    @override
    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def split_nodes_delimiter(old_nodes: list[TextNode], text_type: TextType) -> list[TextNode]:
    # Nothing to do if type TEXT was passed
    if text_type is TextType.TEXT:
        return old_nodes

    if text_type is TextType.LINK or text_type is TextType.IMAGE:
        raise ValueError(f"Cannot split {text_type} with this function")

    pattern: str = '|'.join(re.escape(d) for d in get_delimiters(text_type))

    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        split_node_text: list[str] = re.split(pattern, node.text)

        if len(split_node_text) % 2 != 1:
            raise ValueError("Invalid markdown: Formatted section not closed!")

        # NOTE: You should always split bold before you try italic as the
        #       delimiter for italic (*) can conflict with bold (**)
        for i, text in enumerate(split_node_text):
            new_text_type = TextType.TEXT if i % 2 == 0 else text_type
            new_nodes.append(TextNode(text, new_text_type))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        images: list[tuple[str, str]] = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue

        pattern: str = '|'.join(
            re.escape(f"![{alt_text}]({url})") for alt_text, url in images
        )
        split_node_text: list[str] = re.split(pattern, node.text)

        # Ensure the text and image lists are the same length
        while len(split_node_text) > len(images):
            images.append(("", ""))

        for text, image in zip(split_node_text, images):
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
            alt_text, url = image
            if alt_text != "" and url != "":
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(node)
            continue

        links: list[tuple[str, str]] = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue

        pattern: str = '|'.join(
            "(?<!!)" + re.escape(f"[{alt}]({url})") for alt, url in links
        )
        split_node_text: list[str] = re.split(pattern, node.text)

        # Ensure the text and link lists are the same length
        while len(split_node_text) > len(links):
            links.append(("", ""))

        for text, link in zip(split_node_text, links):
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))
            link_name, url = link
            if link_name != "" and url != "":
                new_nodes.append(TextNode(link_name, TextType.LINK, url))

    return new_nodes
