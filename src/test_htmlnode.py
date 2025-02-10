import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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
    def test_to_html_with_tag(self):
        node = LeafNode("h1", "Hello World!", props={"class": "hello"})
        self.assertEqual(node.to_html(), '<h1 class="hello">Hello World!</h1>')

    def test_to_html_without_tag(self):
        node = LeafNode(None, "value")
        self.assertEqual(node.to_html(), "value")

    def test_repr(self):
        node = LeafNode("p", "What a strange world", {"class": "primary"})
        self.assertEqual(
            node.__repr__(),
            "LeafNode(p, What a strange world, {'class': 'primary'})",
        )


class TestParentNode(unittest.TestCase):
    def test_repr(self):
        node = ParentNode("p", [LeafNode("b", "Bold text")], {"class": "info"})
        self.assertEqual(
            node.__repr__(),
            "ParentNode(p, [LeafNode(b, Bold text, None)], {'class': 'info'})",
        )

    def test_to_html_no_tag(self):
        node = ParentNode(None, [LeafNode("p", "paragraph")])
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_no_children(self):
        node = ParentNode("p", None)
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_only_leaves(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
            {"class": "info"},
        )
        self.assertEqual(
            node.to_html(),
            '<p class="info"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>',
        )

    def test_to_html_parent_as_child(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                ParentNode(
                    "span",
                    [
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                ),
            ],
            {"class": "info"},
        )
        self.assertEqual(
            node.to_html(),
            '<p class="info"><b>Bold text</b>Normal text<span><i>italic text</i>Normal text</span></p>',
        )

    def test_to_html_multiple_parents(self):
        node = node = ParentNode(
            "div",
            [
                LeafNode("div", "Unordered list"),
                ParentNode(
                    "ul", [LeafNode("li", "ul item"), LeafNode("li", "ul item")]
                ),
                LeafNode("div", "Ordered list"),
                ParentNode(
                    "ol", [LeafNode("li", "ol item1"), LeafNode("li", "ol item2")]
                ),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><div>Unordered list</div><ul><li>ul item</li><li>ul item</li></ul><div>Ordered list</div><ol><li>ol item1</li><li>ol item2</li></ol></div>",
        )

    def test_to_html_nested_parents(self):
        node = node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        ParentNode("span", [LeafNode("i", "italic text")]),
                    ],
                    {"class": "info"},
                )
            ],
            {"class": "container"},
        )
        self.assertEqual(
            node.to_html(),
            '<div class="container"><p class="info"><b>Bold text</b>Normal text<span><i>italic text</i></span></p></div>',
        )


if __name__ == "__main__":
    unittest.main()
