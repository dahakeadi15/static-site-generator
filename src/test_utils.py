import unittest

from htmlnode import LeafNode
from textnode import TextNode, TextType
from utils import text_node_to_html_node


class TestUtils(unittest.TestCase):
    def test_text_to_html_text(self):
        text_node = TextNode("normal text", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, text_node.text)

    def test_bold_to_html_bold(self):
        text_node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, text_node.text)
        self.assertEqual(html_node.tag, "b")

    def test_italic_to_html_italic(self):
        text_node = TextNode("italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, text_node.text)
        self.assertEqual(html_node.tag, "i")

    def test_code_to_html_code(self):
        text_node = TextNode("code text", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, text_node.text)
        self.assertEqual(html_node.tag, "code")

    def test_link_to_html_link(self):
        text_node = TextNode("anchor text", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, text_node.text)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": text_node.url})

    def test_image_to_html_image(self):
        text_node = TextNode("italic text", TextType.IMAGE, "/placeholder-image.jpg")
        html_node = text_node_to_html_node(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src": text_node.url, "alt": text_node.text})
