from textnode import TextNode, TextType
from htmlnode import HTMLNode


def main():
    text_node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(text_node)
    text_node = HTMLNode(
        "a",
        "anchor text",
        [HTMLNode("span", "child"), HTMLNode("b", "bold child")],
        {"href": "http://boot.dev", "target": "_blank"},
    )
    print(text_node)


if __name__ == "__main__":
    main()
