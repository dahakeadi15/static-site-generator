import unittest

from block_md_utils import block_to_block_type, markdown_to_blocks


class TestSplitBlocks(unittest.TestCase):
    def test_md_to_blocks(self):
        md_doc = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""
        blocks = markdown_to_blocks(md_doc)
        self.assertListEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
            ],
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )


class TestMdToBlocks(unittest.TestCase):
    def test_heading_to_block(self):
        h1 = "# Heading"
        h2 = "## Heading"
        h3 = "### Heading"
        h4 = "#### Heading"
        h5 = "##### Heading"
        h6 = "###### Heading"
        type_1 = block_to_block_type(h1)
        type_2 = block_to_block_type(h2)
        type_3 = block_to_block_type(h3)
        type_4 = block_to_block_type(h4)
        type_5 = block_to_block_type(h5)
        type_6 = block_to_block_type(h6)
        self.assertListEqual(
            [type_1, type_2, type_3, type_4, type_5, type_6],
            ["heading"] * 6,
        )

    def test_code_to_block(self):
        code = "```\ncode;\nblock;\n# comments\n// more comments\n```"
        block_type = block_to_block_type(code)
        self.assertEqual(block_type, "code")

    def test_quote_to_block(self):
        quote = "> quote first line\n> quote next line\n> - author"
        block_type = block_to_block_type(quote)
        self.assertEqual(block_type, "quote")

    def test_ul_to_block(self):
        ul = "* ul item 1\n- ul item 2"
        block_type = block_to_block_type(ul)
        self.assertEqual(block_type, "unordered_list")

    def test_ol_to_block(self):
        ol = "1. ol item 1\n2. ol item 2\n3. ol item 3"
        block_type = block_to_block_type(ol)
        self.assertEqual(block_type, "ordered_list")

    def test_paragraph_to_block(self):
        para = "normal paragraph\nblock"
        block_type = block_to_block_type(para)
        self.assertEqual(block_type, "paragraph")


if __name__ == "__main__":
    unittest.main()
