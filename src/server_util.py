import os
import shutil

def migrate_files(src, dest):
    src = os.path.abspath(src)
    #dest = os.path.abspath(dest)
    print(f"copying {src} to {dest}")
    if os.path.exists(dest):
        print(f"purging {dest}")
        shutil.rmtree(dest)
        print("purged")
    os.mkdir(dest)
    paths = os.listdir(src)
    for cur_path in paths:
        full_path = os.path.join(src, cur_path)
        full_dest_path = os.path.join(dest, cur_path)
        if os.path.isfile(full_path):
            print(f"copying file {full_path} to {full_dest_path}")
            shutil.copy(full_path, full_dest_path)
        else:
            print(f"copying folder {full_path} to {full_dest_path}")
            os.mkdir(full_dest_path)
            migrate_files(full_path, full_dest_path)

