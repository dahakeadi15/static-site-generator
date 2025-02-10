import unittest

from textnode import TextNode, TextType
from textnode_utils import split_nodes_delimiter


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
