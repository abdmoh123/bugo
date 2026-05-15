import re


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    img_regex = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(img_regex, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    link_regex = r"(?<!!)\[(.*?)\]\((.*?)\)"
    return re.findall(link_regex, text)
