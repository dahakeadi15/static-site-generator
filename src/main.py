import sys

from copystatic import copy_static_to_public
from generatepage import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    # Delete public dir and create fresh, then copy static contents to it
    copy_static_to_public(dir_path_static, dir_path_public, logging=True)

    args = sys.argv
    basepath = "/"
    if len(args) > 1:
        basepath = args[1]

    # generate pages from content and place in public
    print("Generating content...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)
    print("...finished generating content")


if __name__ == "__main__":
    main()
