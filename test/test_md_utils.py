import unittest

from src.md_utils import extract_markdown_images, extract_markdown_links


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


if __name__ == "__main__":
    _ = unittest.main()
