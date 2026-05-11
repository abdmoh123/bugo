import unittest

from src.htmlnode import HTMLNode, HTMLTag, HTMLTagType, LeafNode, ParentNode


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


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode(HTMLTag(HTMLTagType.SPAN), "child")
        parent_node = ParentNode(HTMLTag(HTMLTagType.DIV), [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode(HTMLTag(HTMLTagType.B), "grandchild")
        child_node = ParentNode(HTMLTag(HTMLTagType.SPAN), [grandchild_node])
        parent_node = ParentNode(HTMLTag(HTMLTagType.DIV), [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_multi_children(self):
        child_node1 = LeafNode(HTMLTag(HTMLTagType.SPAN), "child1")
        child_node2 = LeafNode(HTMLTag(HTMLTagType.SPAN), "child2")
        parent_node = ParentNode(HTMLTag(HTMLTagType.DIV), [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child1</span><span>child2</span></div>",
        )

    def test_to_html_with_multi_grandchildren(self):
        child_node1 = LeafNode(HTMLTag(HTMLTagType.SPAN), "child")
        grandchild_node1 = LeafNode(None, "grandchild1")
        grandchild_node2 = LeafNode(HTMLTag(HTMLTagType.B), "grandchild2")
        mid_node = ParentNode(HTMLTag(HTMLTagType.P), [grandchild_node1, grandchild_node2])
        parent_node = ParentNode(HTMLTag(HTMLTagType.DIV), [child_node1, mid_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child</span><p>grandchild1<b>grandchild2</b></p></div>",
        )

    def test_to_html_no_children(self):
        parent_node = ParentNode(HTMLTag(HTMLTagType.DIV), [])
        self.assertEqual(parent_node.to_html(), "<div></div>")


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
