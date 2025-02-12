from copystatic import copy_static_to_public

dir_path_static = "static"
dir_path_public = "public"


def main():
    copy_static_to_public(dir_path_static, dir_path_public, logging=True)


if __name__ == "__main__":
    main()
