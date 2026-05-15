import unittest

from src.textnode import TextNode, TextType, split_nodes_delimiter, split_nodes_image, split_nodes_link


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, None)
        self.assertEqual(node, node2)

    def test_eq_text_fail(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_type_fail(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_url_fail(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_eq_all_fail(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        node2 = TextNode("This is another text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_bold_delimiter(self):
        node = TextNode("This is some **bold** text", TextType.TEXT)
        split_nodes = split_nodes_delimiter([node], TextType.BOLD)
        self.assertEqual(len(split_nodes), 3)
        self.assertEqual(split_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(split_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(split_nodes[2].text_type, TextType.TEXT)

    def test_split_nodes_bold_with_italic_delimiter(self):
        node = TextNode("This is some **bold** and *italic* text", TextType.TEXT)
        split_nodes = split_nodes_delimiter(
            split_nodes_delimiter([node], TextType.BOLD), TextType.ITALIC
        )
        self.assertEqual(len(split_nodes), 5)
        self.assertEqual(split_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(split_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(split_nodes[2].text_type, TextType.TEXT)
        self.assertEqual(split_nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(split_nodes[4].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_none(self):
        node = TextNode("This is regular text", TextType.TEXT)
        split_nodes_bold = split_nodes_delimiter([node], TextType.BOLD)
        split_nodes_italic = split_nodes_delimiter([node], TextType.ITALIC)
        split_nodes_code = split_nodes_delimiter([node], TextType.CODE)
        split_nodes_text = split_nodes_delimiter([node], TextType.TEXT)
        res_array = [
            split_nodes_bold,
            split_nodes_italic,
            split_nodes_code,
            split_nodes_text
        ]
        for res in res_array:
            self.assertEqual(len(res), 1)
            self.assertEqual(node, res[0])
            self.assertEqual(res[0].text_type, TextType.TEXT)

    def test_split_nodes_delimiter_formatting(self):
        node = TextNode("This is *broken text", TextType.TEXT)
        with self.assertRaises(ValueError) as ctx:
            _ = split_nodes_delimiter([node], TextType.ITALIC)
        self.assertIn(
            "Invalid markdown: Formatted section not closed!",
            str(ctx.exception)
        )


class TestSplitNodesImageLink(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_image_first(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_image_surround(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_image_between(self):
        node = TextNode(
            "image to right ![image](https://i.imgur.com/zjjcJKZ.png) image to left",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image to right ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" image to left", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_link_first(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) and another text",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_link_surround(self):
        node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_link_between(self):
        node = TextNode(
            "link to right [link](https://i.imgur.com/zjjcJKZ.png) link to left",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link to right ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" link to left", TextType.TEXT),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    _ = unittest.main()
