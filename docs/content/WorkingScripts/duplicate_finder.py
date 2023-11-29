#!/usr/bin/env python3
"""
TODO:
    Implement Version 
    Elobrate help
    Exclude file patterns
    System folders, don't delete
"""
import os
import argparse
import json
from hashlib import sha256, md5
from collections import OrderedDict

from report_progress import report_progress_basic

exclude_list = (".DS_Store", )

def find_sz_duplicate(folders):
    """
    Scan all the folders, group files based on the size,
    and returns a dictonary with group of files that has 
    same size. the key for each group is file size.
    """
    size_dict = OrderedDict()
    progress = report_progress_basic()
    for folder in folders:
        for subdir, dirs, files in os.walk(folder):
            for filename in files:
                if filename not in exclude_list:
                    filepath = subdir + os.sep + filename
                    file_size = os.path.getsize(filepath)
                    if not file_size in size_dict.keys():
                        size_dict[file_size] = []
                    size_dict[file_size].append(filepath)
                    progress.update(lap_after=2000)
    keys = list(size_dict.keys())
    progress.lap()
    for key in keys:
        if len(size_dict[key]) == 1:
            # remove as there is No duplicate
            del size_dict[key]
    return size_dict


def find_hash(file, minimum=False, blocksize=8 * 1024):
    """
    Find hash for a file, if minimum is True,it finds sha256 
    for first blocksize bytes, else, it finds 
    md5 for entire file. 
    TODO: use smaller blocks when finding md5 for entire file
    """
    with open(file, 'rb') as afile:
        if minimum:
            h = sha256()
            buf = afile.read(blocksize)
            h.update(buf)
            return h.hexdigest()
        else:
            h = md5()
            buf = afile.read()
            h.update(buf)
        return h.hexdigest()


def hash_analysis(sz_dup, minimum=False):
    """
    update the input dictionary with hash

    """
    sz_keys = list(sz_dup.keys())
    progress = report_progress_basic(len(sz_keys))
    for sz in sz_keys:
        hash_dict = OrderedDict()
        for file in sz_dup[sz]:
            hash = find_hash(file, minimum=minimum)
            if not hash in hash_dict.keys():
                hash_dict[hash] = []
            hash_dict[hash].append(file)
        h_keys = list(hash_dict.keys())
        for key in h_keys:
            if len(hash_dict[key]) == 1:
                del hash_dict[key]
        h_keys = list(hash_dict.keys())
        for key in h_keys:
            if len(hash_dict[key]) > 1:
                prefix = str(sz).split('_')[0]
                sz_hash = prefix + "_" + str(key)
                sz_dup[sz_hash] = hash_dict[key]
        del sz_dup[sz]
        progress.update(lap_after=2000)
    progress.lap()
    return sz_dup


def dup_count(dup_lists):
    """
    Counts the number of duplicates
    """
    count = 0
    for dup in dup_lists:
        count = count + len(dup_lists[dup]) - 1
    return count


def confirm_with_system_diff(dup_lists):
    """
    for each duplicate file, invoke diff utility and confirm 
    our finding is correct. This step is redundent, keeping 
    it for testing. May be removed later.
    """
    progress = report_progress_basic(dup_count(dup_lists))
    for dup in dup_lists:
        ref = dup_lists[dup][0]
        for t in dup_lists[dup][1:]:

            cmd = "diff '{}' '{}'".format(ref, t)
            #print(cmd)
            ret_value = os.system(cmd)
            if ret_value != 0:
                print("Failed, check again.....")
                cmd = "diff -s '{}' '{}'".format(ref, t)
                print(cmd)
                os.system(cmd)
                return False
            progress.update(lap_after=2000)
    progress.lap()
    return True


def delete_dups(dup_lists):
    """
    Leave the first entry and delete (remove the file from filesystem)
    all other files. Call this function carefully, it will destroy 
    your files, if called incorrectly.
    """
    # should we check date and decide which is oldest?
    dups = list(dup_lists.keys())

    progress = report_progress_basic(dup_count(dup_lists))
    for dup in dups:
        for t in dup_lists[dup][1:]:
            os.remove(t)
            progress.update()
        del dup_lists[dup]
    progress.lap()


def find_and_delete_duplicate(folders, remove=False):
    """
    finds the duplicate file and removes it if asked for.
    TODO: Use timer, create a clean log for analysis
    """
    print("Scan the folders for sizes")
    sz_dup = find_sz_duplicate(folders)
    print("Size match found for ", dup_count(sz_dup), " + ",
          len(sz_dup.keys()), " files in ", len(sz_dup.keys()), "groups")

    if len(sz_dup.keys()) > 0:
        print("Use quick hash to find duplicates (sha256 algo)")
        sz_dup = hash_analysis(sz_dup, minimum=True)
        print(dup_count(sz_dup),  " potential duplicates found in ",
              len(sz_dup.keys()), "groups")

    if len(sz_dup.keys()) > 0:
        print("Use full hash to confirm (md5)")
        sz_dup = hash_analysis(sz_dup, minimum=False)
        print(dup_count(sz_dup),  "  duplicates  found in ",
              len(sz_dup.keys()), "groups")

    if len(sz_dup.keys()) == 0:
        print("No duplicates found")
    else:
        with open("duplicates.json", "w") as f:
            print(json.dumps(sz_dup), file=f)
        print("run diff utility to double confirm the duplicates")
        duplicates_confirmed = confirm_with_system_diff(sz_dup)
        if duplicates_confirmed and remove:
            print("Deleting duplicate files")
            delete_dups(sz_dup)
        elif not remove:
            print("No file deleted (called in dry_run mode)")
        else:
            print("Warning! Algo failed, detected false duplicate, May be bug in the algorithm, recheck the implementation or contact developer")
            print("No file deleted")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("folders", nargs='+',
                        help="the folder that should be processed")
    parser.add_argument('--remove_duplicates', action='store_true')
    args = parser.parse_args()
    print("Folders: ", args.folders)
    print("args.remove_duplicates = ", args.remove_duplicates)
    find_and_delete_duplicate(args.folders, remove=args.remove_duplicates)
