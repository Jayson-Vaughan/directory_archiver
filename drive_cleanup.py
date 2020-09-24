# Program to traverse directories and archive files not modified since a specified date

import time
import os
import shutil

SECONDS = 267 * 24 * 60 * 60  # time since specified date in seconds (632)
src = 'C:/Users/jvaug/Desktop/cleanup_test'
dst = 'C:/Users/jvaug/Desktop/cleanup_test/Archive'


now = time.time()
before = now - SECONDS


def last_mod_time(fname):  # function to find the last modified date of files
    return os.path.getmtime(fname)


shutil.copytree(src, dst)  # copies directory to archive folder
exclude = set(['Archive'])  # can set exclusions for os.walk()


for root, dirs, files in os.walk(dst):  # walk directory to identify all files/folders
    for fname in files:
        file_path = os.path.join(root, fname)
        if last_mod_time(file_path) > before:  # if file was modified since specified date
            os.unlink(file_path)  # remove from archive folder

for root, dirs, files in os.walk(dst):
    for folders in dirs:
        try:
            folder_path = os.path.join(root, folders)
            print('Empty folder deleted from archive: ' + folder_path)
            os.rmdir(folder_path)
        except OSError:
            continue

for root, directories, files in os.walk(src, topdown=True):
    # excludes any directories from exclusion set
    directories[:] = [d for d in directories if d not in exclude]
    for fname in files:
        file_path = os.path.join(root, fname)
        if last_mod_time(file_path) < before:  # if file not modified since specified date
            print('File archived from directory: ' + file_path)
            os.unlink(file_path)  # removes archived file from directory


for root, directories, files in os.walk(src):
    directories[:] = [d for d in directories if d not in exclude]
    for dirs in directories:
        try:
            dir_path = os.path.join(root, dirs)
            print('Empty Folder Deleted from directory: ' + dir_path)
            os.rmdir(dir_path)  # deletes now empty folders in directory
        except OSError:
            continue  # continues if it finds a folder that is not empty
