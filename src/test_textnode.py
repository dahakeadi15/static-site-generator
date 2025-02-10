import unittest

from htmlnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is text node", TextType.TEXT, "https://boot.dev")
        node2 = TextNode("This is text node", TextType.TEXT, "https://boot.dev")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://boot.dev")
        node2 = TextNode("This is text node2", TextType.BOLD, "https://github.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_diff_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_diff_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_not_eq_diff_url(self):
        node = TextNode("This is another text node", TextType.BOLD, "https://boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://github.com")
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, bold, https://boot.dev)", repr(node)
        )

    def test_false_repr(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://boot.dev")
        self.assertNotEqual("TextNode()", repr(node))


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_to_html_text(self):
        text_node = TextNode("normal text", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)

        self.assertIsInstance(html_node, LeafNode)

        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "normal text")
        self.assertEqual(html_node.children, None)
        self.assertEqual(html_node.props, None)

    def test_bold_to_html_bold(self):
        text_node = TextNode("bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)

        self.assertIsInstance(html_node, LeafNode)

        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold text")
        self.assertEqual(html_node.children, None)
        self.assertEqual(html_node.props, None)

    def test_italic_to_html_italic(self):
        text_node = TextNode("italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)

        self.assertIsInstance(html_node, LeafNode)

        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic text")
        self.assertEqual(html_node.children, None)
        self.assertEqual(html_node.props, None)

    def test_code_to_html_code(self):
        text_node = TextNode("code text", TextType.CODE)
        html_node = text_node_to_html_node(text_node)

        self.assertIsInstance(html_node, LeafNode)

        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "code text")
        self.assertEqual(html_node.children, None)
        self.assertEqual(html_node.props, None)

    def test_link_to_html_link(self):
        text_node = TextNode("anchor text", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(text_node)

        self.assertIsInstance(html_node, LeafNode)

        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "anchor text")
        self.assertEqual(html_node.children, None)
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})

    def test_image_to_html_image(self):
        text_node = TextNode("alt text", TextType.IMAGE, "/placeholder-image.png")
        html_node = text_node_to_html_node(text_node)

        self.assertIsInstance(html_node, LeafNode)

        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.children, None)
        self.assertEqual(
            html_node.props, {"src": "/placeholder-image.png", "alt": "alt text"}
        )

    def test_raises_error(self):
        text_node = TextNode("text", "Heading")
        self.assertRaises(ValueError, lambda: text_node_to_html_node(text_node))


if __name__ == "__main__":
    unittest.main()
