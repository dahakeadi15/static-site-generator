import unittest

from textnode import TextNode, TextType


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


if __name__ == "__main__":
    unittest.main()
