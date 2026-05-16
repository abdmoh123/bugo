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
    heading_pattern = r"^#{1,6} .*$"
    if re.match(heading_pattern, block):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        return BlockType.QUOTE

    # Check for lists
    split_block = block.split("\n")
    norm_list_pattern = r"^(- |\* )(.*)$"
    if all(re.match(norm_list_pattern, line) for line in split_block):
        return BlockType.UNORDERED_LIST

    num_list_pattern = r"^\d+\. .*$"
    if all(re.match(num_list_pattern, line)for line in split_block):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
