import unittest

from htmlnode import ParentNode
from md_to_html import markdown_to_html_node


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
