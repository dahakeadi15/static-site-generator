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


def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_nodes = []

        text = old_node.text
        images = extract_markdown_images(text)

        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        for image in images:
            sections = text.split(f"![{image[0]}]({image[1]})")
            if len(sections) != 2:
                raise ValueError("invalid markdown: image section not closed")
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            split_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            text = sections[1]

        if text != "":
            split_nodes.append(TextNode(text, TextType.TEXT))

        new_nodes.extend(split_nodes)

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue

        split_nodes = []

        text = old_node.text
        links = extract_markdown_links(text)

        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        for link in links:
            sections = text.split(f"[{link[0]}]({link[1]})")
            if len(sections) != 2:
                raise ValueError("invalid markdown: link section not closed")
            if sections[0] != "":
                split_nodes.append(TextNode(sections[0], TextType.TEXT))
            split_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            text = sections[1]

        if text != "":
            split_nodes.append(TextNode(text, TextType.TEXT))

        new_nodes.extend(split_nodes)

    return new_nodes
