import unittest

from src.markdown import BlockType, block_to_block_type, extract_markdown_images, extract_markdown_links, markdown_to_blocks


class TestMDUtils(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_no_images(self):
        matches = extract_markdown_images(
            "This is text with no images"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://boot.dev)"
        )
        self.assertListEqual([("link", "https://boot.dev")], matches)

    def test_extract_markdown_no_links(self):
        matches = extract_markdown_links(
            "This is text with no links"
        )
        self.assertListEqual([], matches)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_extra_newlines(self):
        md = """
Test line.


Second test line.



Third test line.
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Test line.", "Second test line.", "Third test line."])


class TestBlockToBlockType(unittest.TestCase):
    def test_unordered_list(self):
        block = """- You missed that one
- Try another"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = """1. You missed that one
2. Try another"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_headings(self):
        blocks = [
            "# Heading 1",
            "## Heading 2",
            "### Heading 3",
            "#### Heading 4",
            "##### Heading 5",
            "###### Heading 6",
        ]
        expected = [BlockType.HEADING] * 6
        block_types = [block_to_block_type(block) for block in blocks]
        self.assertEqual(block_types, expected)

    def test_not_headings(self):
        blocks = [
            "#this_is_not_a_heading_but_a_tag", "####### Invalid Heading 7",
        ]
        block_types = [block_to_block_type(block) for block in blocks]
        expected = [BlockType.PARAGRAPH] * 2
        self.assertEqual(block_types, expected)

    def test_code(self):
        block = """```python
print('hello world')
print('foo bar')
```"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_quote(self):
        block = """> be me
> create a test case following green text format
> be embarassed in a few minutes"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_paragraph(self):
        block = """This is a paragraph block
This is also multi-line
There are no lists here
Nor code blocks
Nor headings or quotes"""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)


if __name__ == "__main__":
    _ = unittest.main()
