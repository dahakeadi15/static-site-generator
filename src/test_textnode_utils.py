import unittest

from textnode import TextNode, TextType
from textnode_utils import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_block(self):
        node1 = TextNode("This is text with a `code block`", TextType.TEXT)
        node2 = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        self.assertEqual(
            repr(new_nodes),
            repr(
                [
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode("This is text with a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" word", TextType.TEXT),
                ]
            ),
        )

    def test_bold(self):
        node1 = TextNode("This is text with some **bold**", TextType.TEXT)
        node2 = TextNode("This is text with some **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        self.assertEqual(
            repr(new_nodes),
            repr(
                [
                    TextNode("This is text with some ", TextType.TEXT),
                    TextNode("bold", TextType.BOLD),
                    TextNode("This is text with some ", TextType.TEXT),
                    TextNode("bold", TextType.BOLD),
                    TextNode(" text", TextType.TEXT),
                ]
            ),
        )

    def test_italic(self):
        node1 = TextNode("This is text with some *italic*", TextType.TEXT)
        node2 = TextNode("This is text with some *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "*", TextType.ITALIC)
        self.assertEqual(
            repr(new_nodes),
            repr(
                [
                    TextNode("This is text with some ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode("This is text with some ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" text", TextType.TEXT),
                ]
            ),
        )


class Test(unittest.TestCase):
    def test_extract_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extracted_images = extract_markdown_images(text)
        self.assertEqual(
            extracted_images,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_extract_images_with_extra_bracket(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [some text in brackets]"
        extracted_images = extract_markdown_images(text)
        self.assertEqual(
            extracted_images, [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        )

    def test_extract_images_with_extra_parenthesis(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and (some text in brackets)"
        extracted_images = extract_markdown_images(text)
        self.assertEqual(
            extracted_images, [("rick roll", "https://i.imgur.com/aKaOqIh.gif")]
        )

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        extracted_links = extract_markdown_links(text)
        self.assertEqual(
            extracted_links,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_extract_links_with_extra_bracket(self):
        text = "This is text with [just some bracketed text], a link [to boot dev](https://www.boot.dev) and [some more]."
        extracted_links = extract_markdown_links(text)
        self.assertEqual(extracted_links, [("to boot dev", "https://www.boot.dev")])

    def test_extract_links_with_extra_parenthesis(self):
        text = "This is text with (just some bracketed text), a link [to boot dev](https://www.boot.dev) and (some more)."
        extracted_links = extract_markdown_links(text)
        self.assertEqual(extracted_links, [("to boot dev", "https://www.boot.dev")])


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
