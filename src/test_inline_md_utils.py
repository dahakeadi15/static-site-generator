import unittest

from inline_md_utils import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


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


class TestExtractingImagesAndLinks(unittest.TestCase):
    # IMAGES
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

    def test_extract_images_not_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and an image ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extracted_images = extract_markdown_images(text)
        self.assertEqual(
            extracted_images, [("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        )

    # LINKS

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

    def test_extract_links_not_images(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and an image ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        extracted_links = extract_markdown_links(text)
        self.assertEqual(extracted_links, [("to boot dev", "https://www.boot.dev")])


class TestSplitImages(unittest.TestCase):
    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode(
                    "rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"
                ),
                TextNode(" and ", TextType.TEXT),
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_split_nodes_images_exclude_links(self):
        node = TextNode(
            "This is text with an image ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an image ", TextType.TEXT),
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(
                    " and a link [to boot dev](https://www.boot.dev)",
                    TextType.TEXT,
                ),
            ],
        )

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode("![image](https://www.example.COM/IMAGE.PNG)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG")],
            new_nodes,
        )


class TestSplitLinks(unittest.TestCase):
    def test_split_nodes_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )

    def test_split_nodes_links_exclude_images(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and an image ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(
                    " and an image ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
                    TextType.TEXT,
                ),
            ],
        )


class TestTextToTextNode(unittest.TestCase):
    def test_text_to_textnode(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        textnodes = text_to_textnodes(text)
        self.assertListEqual(
            textnodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )


# Lane's solution
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
