import os
import shutil


def copy_static_to_public(path_static, path_public, logging=False):
    if logging:
        print("Deleting public directory...")
    if os.path.exists(path_public):
        shutil.rmtree(path_public)
    if logging:
        print("...completed deleting")

    if logging:
        print("Copying static files to public directory...")
    copy_files_recursive(path_static, path_public, logging)
    if logging:
        print("...completed copying")


def copy_files_recursive(src, dest, logging=False):
    if not os.path.exists(dest):
        os.mkdir(dest)
        if logging:
            print(f"> created dir : {dest}")

    dir_list = os.listdir(src)

    for item in dir_list:
        src_path = os.path.join(src, item)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest)
            if logging:
                print(f"> copied      : {item} > {dest}")
        else:
            dest_path = os.path.join(dest, item)
            copy_files_recursive(src_path, dest_path, logging)
