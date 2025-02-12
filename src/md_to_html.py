from block_md_utils import block_to_block_type, markdown_to_blocks
from htmlnode import LeafNode, ParentNode
from inline_md_utils import text_to_textnodes
from textnode import TextNode, text_node_to_html_node


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    root_node = ParentNode("div", [])

    for block in blocks:
        block_node = md_block_to_html_block(block)
        root_node.children.append(block_node)

    return root_node


def md_block_to_html_block(block):
    block_type = block_to_block_type(block)
    block_lines = block.split("\n")
    children = None

    match block_type:
        case "heading":
            level, heading = block.split(" ", maxsplit=1)
            tag = f"h{len(level)}"
            block_lines = [heading]
            children = block_text_to_children_nodes(block_lines)
        case "paragraph":
            tag = "p"
            children = block_text_to_children_nodes(block_lines)
        case "code":
            tag = "pre"
            children = [LeafNode("code", "\n".join(block_lines[1:-1]))]
        case "quote":
            tag = "blockquote"
            block_lines = [line.split("> ", maxsplit=1)[1] for line in block_lines]
            children = block_text_to_children_nodes(block_lines)
        case "unordered_list":
            tag = "ul"
            lines = []
            for line in block_lines:
                if line.startswith("* "):
                    lines.append(line.split("* ", maxsplit=1)[1])
                elif line.startswith("- "):
                    lines.append(line.split("- ", maxsplit=1)[1])
                else:
                    lines.append(line)
            children = [
                ParentNode("li", [b]) for b in block_text_to_children_nodes(lines)
            ]
        case "ordered_list":
            tag = "ol"
            lines = []
            i = 1
            for line in block_lines:
                lines.append(line.split(f"{i}. ", maxsplit=1)[1])
                i += 1
            children = [
                ParentNode("li", [b]) for b in block_text_to_children_nodes(lines)
            ]
        case _:
            raise ValueError("invalid markdown: block not supported")

    return ParentNode(tag, children)


def block_text_to_children_nodes(lines):
    nodes = []
    for line in lines:
        text_nodes = text_to_textnodes(line)
        for text_node in text_nodes:
            nodes.append(text_node_to_html_node(text_node))
    return nodes
