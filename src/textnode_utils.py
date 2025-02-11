import re

from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i, section in enumerate(sections):
            if section == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(section, TextType.TEXT))
            else:
                split_nodes.append(TextNode(section, text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    # my: r"!\[(.*?)\]\((.*?)\)"
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    images = []
    for image in re.findall(pattern, text):
        images.append(image)
    return images


def extract_markdown_links(text):
    # my: r"\[(.[^\[]*?)\]\((.*?)\)" or r"[^!]\[([^\[\]]*?)\]\(([^\(\)]*?)\)"
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"  # all browsers may not support
    links = []
    for link in re.findall(pattern, text):
        links.append(link)
    return links
