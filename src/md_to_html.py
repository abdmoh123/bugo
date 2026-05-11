from src.htmlnode import HTMLNode, HTMLTag, HTMLTagType, LeafNode
from src.textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode(HTMLTag(HTMLTagType.BOLD), text_node.text)
        case TextType.ITALIC:
            return LeafNode(HTMLTag(HTMLTagType.ITALIC), text_node.text)
        case TextType.CODE:
            return LeafNode(HTMLTag(HTMLTagType.CODE), text_node.text)
        case TextType.LINK:
            if (text_node.url is None):
                raise ValueError("URL is None, yet text type is LINK")
            return LeafNode(
                HTMLTag(HTMLTagType.A), text_node.text, {"href": text_node.url}
            )
        case TextType.IMAGE:
            if (text_node.url is None):
                raise ValueError("URL is None, yet text type is IMG")
            return LeafNode(
                HTMLTag(HTMLTagType.IMG),
                "",
                {"src": text_node.url, "alt": text_node.text}
            )
