import unittest

from src.htmlnode import HTMLNode, HTMLTag, HTMLTagType, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single(self):
        node = HTMLNode(props={"href": "https://boot.dev"})
        self.assertEqual(node.props_to_html(), ' href="https://boot.dev"')

    def test_props_to_html_multi(self):
        node = HTMLNode(props={"href": "https://boot.dev", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://boot.dev" target="_blank"')

    def test_props_to_html_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), '')


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode(HTMLTag(HTMLTagType.P), "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_h2(self):
        node = LeafNode(HTMLTag(HTMLTagType.H, 2), "Title")
        self.assertEqual(node.to_html(), "<h2>Title</h2>")

    def test_leaf_to_html_only_value(self):
        node = LeafNode(None, "sample text")
        self.assertEqual(node.to_html(), "sample text")

    def test_leaf_to_html_props(self):
        node = LeafNode(HTMLTag(HTMLTagType.A), "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')


if __name__ == "__main__":
    _ = unittest.main()
