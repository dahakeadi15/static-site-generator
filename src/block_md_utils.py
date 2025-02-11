def markdown_to_blocks(md_document):
    blocks = md_document.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        filtered_blocks.append(block.strip())
    return filtered_blocks
