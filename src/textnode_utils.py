from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []

    for node in old_nodes:
        text = node.text
        type = node.text_type

        delimiter_flag = False
        normal_text = ""
        special_text = ""

        i = 0
        while i < len(text):
            char = text[i]
            if text_type == TextType.BOLD and i != len(text) - 1:
                delimiter_chars = text[i] + text[i + 1]
            else:
                delimiter_chars = char

            i += 1
            # catch normal text
            if not delimiter_flag:
                if delimiter_chars == delimiter:
                    if len(delimiter_chars) == 2:
                        i += 1
                    delimiter_flag = True
                    new_nodes.append(TextNode(normal_text, type))
                    normal_text = ""
                    continue

                normal_text += char

            # catch special text
            else:
                if delimiter_chars == delimiter:
                    if len(delimiter_chars) == 2:
                        i += 1
                    delimiter_flag = False
                    new_nodes.append(TextNode(special_text, text_type))
                    special_text = ""
                    continue

                special_text += char

        if normal_text:
            new_nodes.append(TextNode(normal_text, type))

    return new_nodes
