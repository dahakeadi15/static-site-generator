import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError, node.to_html)

    def test_props_to_html(self):
        node = HTMLNode(props={"href": "https://boot.dev", "target": "_blank"})
        self.assertEqual(
            node.props_to_html(), ' href="https://boot.dev" target="_blank"'
        )

    def test_repr_all(self):
        node = HTMLNode(
            "a",
            "anchor text",
            [HTMLNode("span", "child")],
            {"href": "http://boot.dev", "target": "_blank"},
        )
        self.assertEqual(
            "HTMLNode(a, anchor text, children: [HTMLNode(span, child, children: None, props: None)], props: {'href': 'http://boot.dev', 'target': '_blank'})",
            repr(node),
        )

    def test_repr_none(self):
        node = HTMLNode()
        self.assertEqual(
            "HTMLNode(None, None, children: None, props: None)",
            repr(node),
        )

    # Lane's version
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, props: {'class': 'primary'})",
        )


class TestLeafNode(unittest.TestCase):
    def test_init(self):
        node = LeafNode(value="value", tag="div", props={"class": "property"})
        self.assertIsInstance(node, HTMLNode)

    def test_to_html_with_tag(self):
        node = LeafNode(value="value", tag="div", props={"class": "property"})
        self.assertEqual(node.to_html(), '<div class="property">value</div>')

    def test_to_html_without_tag(self):
        node = LeafNode(value="value")
        self.assertEqual(node.to_html(), "value")


if __name__ == "__main__":
    unittest.main()
