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
        start = 0
        i = 0
        while i < len(images):
            img = images[i]
            img_text = f"![{img[0]}]({img[1]})"
            end = text.index(img_text)
            if start < end:
                split_nodes.append(TextNode(text[start:end], TextType.TEXT))
            else:
                split_nodes.append(TextNode(img[0], TextType.IMAGE, img[1]))
                i += 1
                if i == len(images) and start != len(text):
                    split_nodes.append(TextNode(text[start:], TextType.TEXT))
            start = end + len(img_text)

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
        # sections = re.split(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
        # for section in sections:
        #     if section == "":
        #         continue
        #     if section in links:
        #         print("===|", section)
        start = 0
        i = 0
        while i < len(links):
            link = links[i]
            link_text = f"[{link[0]}]({link[1]})"
            end = text.index(link_text)
            if start < end:
                split_nodes.append(TextNode(text[start:end], TextType.TEXT))
            else:
                split_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                i += 1
                if i == len(links) and start != len(text):
                    split_nodes.append(TextNode(text[start:], TextType.TEXT))
            start = end + len(link_text)

        new_nodes.extend(split_nodes)

    return new_nodes
