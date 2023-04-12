#!/usr/bin/env python3
""" query and organize png files
"""

import traceback, sys, os
from PIL import Image

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def sprint(*args, **kwargs):
    print(*args, file=sys.stdout, **kwargs)
    
    
def show_usage():
    if len(sys.argv) > 1:
        eprint("  I got:", sys.argv)
        eprint("")
    eprint("Usage: "+ os.path.basename(__file__) + " <key> <dest>")

def get_directory_name(parameters):
    kvs = dict()
    for line in parameters.splitlines():
        if line.startswith("Steps"):
            for part in line.split(","):
                kv = part.split(":")
                kvs[kv[0].strip()] = kv[1].strip()
    return kvs["Model"] + "_" + kvs["Steps"] + "_" + kvs["CFG scale"]


def get_directory_name_from_file(file):
    image = Image.open(file)
    image.load()
    return get_directory_name(image.info["parameters"])
    
def move_file(file, destination_dir, destination_file):
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)   
    os.replace(file, destination_file) 


def process_png(file, move = False):
    basename = os.path.basename(file)
    destination_name = get_directory_name_from_file(file)
    destination_dir = os.path.join(os.getcwd(), destination_name)
    destination_file = os.path.join(destination_dir, basename)

    print("  move " + file + " -> " + destination_file)
    if move:
        move_file(file, destination_dir, destination_file)


def get_clean_list(directories):
    result = []
    last = ""
    for dir in reversed(directories):
        if not dir == last:
            result += [dir]
            last = dir
    return result


def removeEmptyFolders(path):
    if not os.path.isdir(path):
        return

    # remove empty subfolders
    files = os.listdir(path)
    if len(files):
        for f in files:
            fullpath = os.path.join(path, f)
            if os.path.isdir(fullpath):
                removeEmptyFolders(fullpath)

    # if folder empty, delete it
    files = os.listdir(path)
    if len(files) == 0:
        print ("Removing empty folder:", path)
        os.rmdir(path)

def remove_directory(path):
    folders = sorted(list(os.walk(path))[1:],reverse=True)
    for folder in folders:
        try:
            os.rmdir(folder[0])
        except OSError as error: 
            print("Directory '{}' can not be removed".format(folder[0])) 

def main():
    print("sys.argv: ", sys.argv)
    if len(sys.argv) == 1:
        eprint(os.path.basename(__file__) + " commandline error: invalid argument(s)\n")
        show_usage()
        sys.exit(1)
    
    apply = False
    if len(sys.argv) > 1: 
        mask = sys.argv[1]

    if len(sys.argv) == 3: # actually apply the operation, not just list what we would do
        apply = True
    
    mask = os.path.realpath(mask)
    print ("mask: ", mask)
    for root, dirs, files in os.walk(mask, topdown=False):
        for name in files:
            fullpath = os.path.join(root, name)
            dummy, extension = os.path.splitext(fullpath)
            if (extension.lower() == ".png"):
                process_png(fullpath, apply)

    if apply:
        removeEmptyFolders(mask)

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        info = traceback.format_exc()
        eprint(info)
        show_usage()
        sys.exit(1)


    