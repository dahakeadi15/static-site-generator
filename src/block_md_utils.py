def markdown_to_blocks(md_document):
    blocks = md_document.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        filtered_blocks.append(block.strip())
    return filtered_blocks


def block_to_block_type(block: str):
    lines = block.split("\n")

    # Heading
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return "heading"

    # Code
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return "code"

    # Quote
    is_quote = True

    for line in lines:
        if not line.startswith("> "):
            is_quote = False
            break

    if is_quote:
        return "quote"

    # Unordered List
    is_ol = True

    for line in lines:
        if not (line.startswith("* ") or line.startswith("- ")):
            is_ol = False
            break

    if is_ol:
        return "unordered_list"

    # Ordered List
    is_ul = True
    i = 1
    for line in lines:
        if not line.startswith(f"{i}."):
            is_ul = False
            break
        i += 1

    if is_ul:
        return "ordered_list"

    # Normal Paragraph
    return "paragraph"
