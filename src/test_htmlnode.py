import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError, node.to_html)

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://boot.dev", "target": "_blank"})
        self.assertEqual(
            node.props_to_html(), ' href="https://boot.dev" target="_blank"'
        )

    def test_props_to_html_false(self):
        node = HTMLNode(props={"href": "https://boot.dev", "target": "_blank"})
        self.assertNotEqual(
            node.props_to_html(), 'href="https://boot.dev" target="_blank"'
        )

    def test_repr_all(self):
        node = HTMLNode(
            "a",
            "anchor text",
            [HTMLNode("span", "child"), HTMLNode("b", "bold child")],
            {"href": "http://boot.dev", "target": "_blank"},
        )
        self.assertEqual(
            "HTMLNode(tag: <a></a>, value: anchor text, number_of_children: 2 HTMLNode(s), props: {'href': 'http://boot.dev', 'target': '_blank'})",
            repr(node),
        )

    def test_repr_none(self):
        node = HTMLNode()
        self.assertEqual(
            "HTMLNode(tag: None, value: None, number_of_children: No HTMLNode(s), props: None)",
            repr(node),
        )

    def test_false_repr(self):
        node = HTMLNode()
        self.assertNotEqual("HTMLNode()", repr(node))


if __name__ == "__main__":
    unittest.main()
