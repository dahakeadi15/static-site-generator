def markdown_to_blocks(md_document):
    blocks = md_document.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        filtered_blocks.append(block.strip())
    return filtered_blocks


def block_to_block_type(block: str):
    # Heading
    if (
        block.startswith("# ")
        or block.startswith("## ")
        or block.startswith("### ")
        or block.startswith("#### ")
        or block.startswith("##### ")
        or block.startswith("###### ")
    ):
        return "heading"

    lines = block.split("\n")

    # Code
    first_line = lines[0]
    last_line = lines[-1]
    if first_line.startswith("```") and last_line.startswith("```"):
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
    prev = 0
    for line in lines:
        index = line.split(" ", maxsplit=1)[0]
        if index[-1] != ".":
            is_ul = False
            break
        curr = int(index[:-1])
        if curr - 1 != prev:
            is_ul = False
            break
        prev = curr

    if is_ul:
        return "ordered_list"

    # Normal Paragraph
    return "paragraph"
