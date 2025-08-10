import os

from md_to_html import markdown_to_html_node


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    dir_list = os.listdir(dir_path_content)
    for item in dir_list:
        src_path = os.path.join(dir_path_content, item)
        if os.path.isfile(src_path):
            if item[-3:] == ".md":
                dest_file_name = item[:-3]
                dest_file_path = os.path.join(dest_dir_path, f"{dest_file_name}.html")
                generate_page(src_path, template_path, dest_file_path, basepath)
        else:
            dest_path = os.path.join(dest_dir_path, item)
            generate_pages_recursive(src_path, template_path, dest_path, basepath)


def generate_page(from_path, template_path, dest_path, basepath):
    print(
        f"Generating page from `{from_path}` to `{dest_path}` using `{template_path}`..."
    )

    with open(from_path) as markdown_file:
        md_content = markdown_file.read()

    with open(template_path) as template_file:
        template = template_file.read()

    html_string = markdown_to_html_node(md_content).to_html()
    page_title = extract_title(md_content)

    page_html = template.replace("{{ Title }}", page_title)
    page_html = page_html.replace("{{ Content }}", html_string)
    page_html = page_html.replace('href="/', f'href="{basepath}')
    page_html = page_html.replace('src="/', f'src="{basepath}')

    dest_dirname = os.path.dirname(dest_path)
    if not os.path.exists(dest_dirname):
        os.makedirs(dest_dirname)

    with open(dest_path, "w") as html_file:
        html_file.write(page_html)

    print("...generated")


def extract_title(markdown):
    title = ""
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            title = line.lstrip("#").strip()
            break
    if title == "":
        raise ValueError("Title not found!")
    return title
