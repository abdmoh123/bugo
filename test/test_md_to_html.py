
import unittest

from src.htmlnode import HTMLTag, HTMLTagType
from src.md_to_html import text_node_to_html_node
from src.textnode import TextNode, TextType


class TestMDToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is italics", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, HTMLTag(HTMLTagType.ITALIC))
        self.assertEqual(html_node.value, "This is italics")

    def test_link(self):
        node = TextNode("hyaa", TextType.LINK, "https://zelda.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, HTMLTag(HTMLTagType.A))
        self.assertEqual(html_node.value, "hyaa")

        self.assertIsNotNone(html_node.props)
        if not html_node.props:
            raise RuntimeError("This shouldn't be reachable")
        self.assertEqual(html_node.props["href"], "https://zelda.com")

    def test_image(self):
        node = TextNode("sample text", TextType.IMAGE, "./sample_image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, HTMLTag(HTMLTagType.IMG))
        self.assertEqual(html_node.value, "")

        self.assertIsNotNone(html_node.props)
        if not html_node.props:
            raise RuntimeError("This shouldn't be reachable")
        self.assertEqual(html_node.props["src"], "./sample_image.png")
        self.assertEqual(html_node.props["alt"], "sample text")


if __name__ == "__main__":
    _ = unittest.main()
