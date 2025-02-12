import os
import shutil

from textnode import TextNode, TextType


def main():
    text_node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    copy_static_to_public()


def copy_static_to_public():
    src = "static"
    dest = "public"
    if os.path.exists(dest):
        shutil.rmtree("public")
    else:
        os.mkdir("public")
    copy_files(src, dest)


def copy_files(src, dest):
    if not os.path.exists(dest):
        os.mkdir(dest)

    dir_list = os.listdir(src)

    for item in dir_list:
        src_path = os.path.join(src, item)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest)
        else:
            dest_path = os.path.join(dest, item)
            copy_files(src_path, dest_path)


if __name__ == "__main__":
    main()
