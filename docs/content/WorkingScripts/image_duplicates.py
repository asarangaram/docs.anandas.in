#!/usr/bin/env python3
import os
import argparse
import json
from hashlib import sha256, md5
from collections import OrderedDict
from pathlib import Path
from typing import ItemsView
from report_progress import report_progress_basic
import re
import subprocess
import time
import datetime


exclude_list = (".DS_Store", )
class metadata():
    def __init__(self, file):
        self.file = file
        self.p = re.compile('\"(\d+)\"\n?')
    def get_best_image_date(self):
        cmd = ['exiftool', '-d', '"%s"', "-AllDates", "{}".format(self.file)]
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        output = result.stdout.decode('latin-1').split("\n")
        for item in range(len(output)):
            if output[item] == '':
                output.pop(item)
        if output == []:
            return None
        d = OrderedDict()
        for item in output:
            if item:
                info_pair = item.split(":")
                if info_pair:
                    d[info_pair[0].strip()] = info_pair[1].strip()
        #print(json.dumps(d, indent=2))

        ts = []
        for item in ["DateTime Original", "CreateDate", "Modify Date"]:
            if item in d.keys():
                if item in d.keys():
                    m = self.p.match(d[item])
                    if m:
                        ts.append(int(m.group(1)))
                else:
                    print(item, " Not found !!!")
                    input()
        if ts:
            return min(ts)
        return None
    def get_best_file_date(self):
        cmd = ['exiftool', '-d', '"%s"', "{}".format(self.file)]
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        output = result.stdout.decode('latin-1').split("\n")
        for item in range(len(output)):
            if output[item] == '':
                output.pop(item)
        
        if output == []:
            return None
        
        d = OrderedDict()
        for item in output:
            if item:
                info_pair = item.split(":")
                if info_pair:
                    d[info_pair[0].strip()] = info_pair[1].strip()
        #print(json.dumps(d, indent=2))
        ts = []
        for item in ["File Access Date/Time", "File Modification Date/Time", "File Inode Change Date/Time"]:
            if item in d.keys():
                if item in d.keys():
                    m = self.p.match(d[item])
                    if m:
                        ts.append(int(m.group(1)))
                else:
                    print(item, " Not found !!!")
                    input()
        if ts:
            return min(ts)
        return None
    def apply_time(self, timestamp):
        #print("------------------ Apply time ------")
        cmd = ['exiftool', '-d', '%s', '-AllDates={}'.format(timestamp), 
                                        '-filecreatedate={}'.format(timestamp), 
                                        '-filemodifydate={}'.format(timestamp),
                "{}".format(self.file)]
        #for i in cmd:
        #    print(i, " ", end="", flush=True)

        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        output = result.stdout.decode('latin-1').split("\n")
        #print(output)
        cmd = ['exiftool',  "-AllDates", "{}".format(self.file)]
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        output = result.stdout.decode('latin-1').split("\n")
        print(output)
       


def name_duplicates(folders):
    name_dups = OrderedDict()
    progress = report_progress_basic()
    
    for folder in folders:
        for subdir, dirs, files in os.walk(folder):
            for filename in files:
                if filename not in exclude_list:
                    filepath = Path(subdir + os.sep + filename)
                    key = re.sub(r" ?\([^)]+\)", "", filepath.stem)
                    if key not in name_dups.keys():
                        name_dups[key] = []
                    name_dups[key].append(str(filepath))
    # print(json.dumps(name_dups, indent = 2))

    for key in name_dups.keys():
        timestampes = []
        for image_file in name_dups[key]:
            md = metadata(image_file)
            ts = md.get_best_image_date()
            if not ts:
                ts = md.get_best_file_date()
            if ts:
                timestampes.append(ts)
               
        if len(timestampes) >= 1:
            ts = min(timestampes)
            print(key, " --> ", time.localtime(ts)) 
            for image_file in name_dups[key]:
                md = metadata(image_file)
                md.apply_time(ts)
                #input()
        else:
            print("key", "-->", "No Time info!")
        #input()
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("folders", nargs='+',
                        help="the folder that should be processed")
    parser.add_argument('--remove_duplicates', action='store_true')
    args = parser.parse_args()
    name_duplicates(args.folders)