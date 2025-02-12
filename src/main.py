import os

from copystatic import copy_static_to_public
from generatepage import generate_page

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    # Delete public dir and create fresh, then copy static contents to it
    copy_static_to_public(dir_path_static, dir_path_public, logging=True)

    # generate page from content and place in public
    content_path = os.path.join(dir_path_content, "index.md")
    public_path = os.path.join(dir_path_public, "index.html")
    generate_page(content_path, template_path, public_path)


if __name__ == "__main__":
    main()
