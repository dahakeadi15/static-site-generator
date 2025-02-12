import os

from copystatic import copy_static_to_public
from generatepage import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    # Delete public dir and create fresh, then copy static contents to it
    copy_static_to_public(dir_path_static, dir_path_public, logging=True)

    # generate pages from content and place in public
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)


if __name__ == "__main__":
    main()
