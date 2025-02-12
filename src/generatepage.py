import os

from md_to_html import extract_title, markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    print(
        f"Generating page from `{from_path}` to `{dest_path}` using `{template_path}`..."
    )

    with open(from_path) as markdown_file:
        md_content = markdown_file.read()

    with open(template_path) as template_file:
        template = template_file.read()

    html_string = markdown_to_html_node(md_content).to_html()
    page_title = extract_title(md_content)

    html_content = template.replace("{{ Title }}", page_title)
    html_content = html_content.replace("{{ Content }}", html_string)

    dest_dirname = os.path.dirname(dest_path)
    if not os.path.exists(dest_dirname):
        os.makedirs(dest_dirname)

    with open(dest_path, "w") as html_file:
        html_file.write(html_content)

    print("...generated")


# Write the new full HTML page to a file at dest_path. Be sure to create any necessary directories if they don’t exist.
