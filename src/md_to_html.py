from block_md_utils import block_to_block_type, markdown_to_blocks
from htmlnode import LeafNode, ParentNode
from inline_md_utils import text_to_textnodes
from textnode import text_node_to_html_node


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    root_node = ParentNode("div", [])

    for block in blocks:
        block_node = block_to_html_node(block)
        root_node.children.append(block_node)

    return root_node


def block_to_html_node(block):
    block_type = block_to_block_type(block)
    block_lines = block.split("\n")
    children = None

    match block_type:
        case "heading":
            level, heading = block.split(" ", maxsplit=1)
            if len(level) > 6:
                raise ValueError(f"invalid heading level: {level}")
            tag = f"h{len(level)}"
            children = text_to_children(heading)
        case "paragraph":
            tag = "p"
            text = " ".join(block_lines)
            children = text_to_children(text)
        case "code":
            tag = "pre"
            children = [LeafNode("code", "\n".join(block_lines[1:-1]))]
        case "quote":
            tag = "blockquote"
            new_lines = []
            for line in block_lines:
                new_lines.append(line.lstrip(">").strip())
            content = " ".join(new_lines)
            children = text_to_children(content)
        case "unordered_list":
            tag = "ul"
            html_items = []
            for item in block_lines:
                text = item[2:]
                item_children = text_to_children(text)
                html_items.append(ParentNode("li", item_children))
            children = html_items
        case "ordered_list":
            tag = "ol"
            html_items = []
            for line in block_lines:
                text = line.split(f" ", maxsplit=1)[1]
                item_children = text_to_children(text)
                html_items.append(ParentNode("li", item_children))
            children = html_items
        case _:
            raise ValueError("invalid markdown: block not supported")

    return ParentNode(tag, children)


def text_to_children(text):
    children = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children


def extract_title(markdown):
    title = ""
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            title = line.lstrip("#").strip()
    if title == "":
        raise ValueError("Title not found!")
    return title
