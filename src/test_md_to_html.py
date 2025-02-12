import unittest

from htmlnode import ParentNode
from md_to_html import extract_title, markdown_to_html_node


class TestMdToHTML(unittest.TestCase):
    def test_md_to_html(self):
        md_document = """
# Heading1

## Heading2

normal paragraph and link to [boot.dev](https://boot.dev)

```
code block
```

> epic quote

![cool image](https://i.imgur.com/aKaOqIh.gif)

* ul item 1
- ul item 2

1. ol item 1
2. ol item 2
"""

        html_node = markdown_to_html_node(md_document)
        self.assertIsInstance(html_node, ParentNode)

        self.assertEqual(
            html_node.to_html(),
            '<div><h1>Heading1</h1><h2>Heading2</h2><p>normal paragraph and link to <a href="https://boot.dev">boot.dev</a></p><pre><code>code block</code></pre><blockquote>epic quote</blockquote><p><img src="https://i.imgur.com/aKaOqIh.gif" alt="cool image"/></p><ul><li>ul item 1</li><li>ul item 2</li></ul><ol><li>ol item 1</li><li>ol item 2</li></ol></div>',
        )

    def test_md_to_html_2(self):
        md_document = """
# Heading1 *Italic* **Bold**

> Hello this is a blockquote *italic* **Bold**. [link](https://google.com)

```
code block **bold** *italic* [link](https://goolge.com)
```

`**bold** *italic* [link](https://goolge.com)`
"""

        html_node = markdown_to_html_node(md_document)
        self.assertIsInstance(html_node, ParentNode)

        self.assertEqual(
            html_node.to_html(),
            '<div><h1>Heading1 <i>Italic</i> <b>Bold</b></h1><blockquote>Hello this is a blockquote <i>italic</i> <b>Bold</b>. <a href="https://google.com">link</a></blockquote><pre><code>code block **bold** *italic* [link](https://goolge.com)</code></pre><p><code>**bold** *italic* [link](https://goolge.com)</code></p></div>',
        )

    # Lane's tests
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_error(self):
        markdown = ""
        self.assertRaises(ValueError, lambda: extract_title(markdown))

    def test_extract_title(self):
        markdown = """
# Tolkien Fan Club

**I like Tolkien**. Read my [first post here](/majesty) (sorry the link doesn't work yet)

> All that is gold does not glitter

## Reasons I like Tolkien

* You can spend years studying the legendarium and still not understand its depths
* It can be enjoyed by children and adults alike
"""
        title = extract_title(markdown)
        self.assertEqual(title, "Tolkien Fan Club")

    def test_extract_title_2(self):
        markdown = """

**I like Tolkien**. Read my [first post here](/majesty) (sorry the link doesn't work yet)

# Tolkien Fan Club

"""
        title = extract_title(markdown)
        self.assertEqual(title, "Tolkien Fan Club")


if __name__ == "__main__":
    unittest.main()
