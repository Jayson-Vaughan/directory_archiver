''' Program to traverse directories and archive files not
    modified since a specified date'''


import time
import os
import shutil


SECONDS = 272 * 24 * 60 * 60  # time since specified date in seconds (1002)
archive = 'Pre-2018 Archive'
src = 'C:/Users/jvaug/Desktop/cleanup_test'
dst = os.path.join(src, archive)


now = time.time()
before = now - SECONDS


# function to find the last modified date of files
def last_mod_time(fname):
    return os.path.getmtime(fname)


shutil.copytree(src, dst)  # copies directory to archive folder
exclude = set([archive])  # can set exclusions for os.walk()


# removes files not to be archived from archive folder
for root, dirs, files in os.walk(dst):
    for fname in files:
        file_path = os.path.join(root, fname)
        if last_mod_time(file_path) > before:
            os.unlink(file_path)


# removes empty folders from the archive folder
for root, dirs, files in os.walk(dst):
    for folders in dirs:
        try:
            folder_path = os.path.join(root, folders)
            os.rmdir(folder_path)
            print('Empty folder deleted from archive: ' + folder_path)
        except OSError as e:
            print('EXCEPTION: ', str(e))
            continue


# removes archived files from directory
for root, dirs, files in os.walk(src, topdown=True):
    dirs[:] = [d for d in dirs if d not in exclude]  # os.walk() exceptions
    for fname in files:
        file_path = os.path.join(root, fname)
        if last_mod_time(file_path) < before:
            os.unlink(file_path)
            print('File archived from directory: ' + file_path)


# deletes now empty folders in the directory
for root, dirs, files in os.walk(src, topdown=False):
    dirs[:] = [d for d in dirs if d not in exclude]
    for folders in dirs:
        try:
            dir_path = os.path.join(root, folders)
            os.rmdir(dir_path)
            print('Empty folder deleted from directory: ' + dir_path)
        except OSError as e:
            print("EXCEPTION: ", str(e))
