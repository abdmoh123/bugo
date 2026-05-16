from enum import StrEnum, auto
import re


class BlockType(StrEnum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    img_regex = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(img_regex, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    link_regex = r"(?<!!)\[(.*?)\]\((.*?)\)"
    return re.findall(link_regex, text)


def markdown_to_blocks(markdown: str) -> list[str]:
    return [block.strip() for block in markdown.split("\n\n") if block != ""]


def block_to_block_type(block: str) -> BlockType:
    if block.startswith("#"):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        return BlockType.QUOTE

    # Check for lists
    split_block = block.split("\n")
    if all(line.startswith("- ") for line in split_block):
        return BlockType.UNORDERED_LIST

    num_regex = r"^\d+\. .*"
    if all(re.match(num_regex, line)for line in split_block):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
