#!/usr/bin/env python3
NOT WORKING .... Using as scratch...

import os
from pathlib import Path
import re
from smart_copy import smart_copy
from file_iterator import Files



from exif import Image
import re
import calendar
import datetime
import time
def str2timestamp(val):
    if val != '0000:00:00 00:00:00':
        p = re.compile('(.*):(.*):(.*)\ (.*):(.*):(.*)')
        m = p.match(val)
        if m:
            return time.mktime(datetime.datetime(
                year=int(m.group(1)), month=int(m.group(2)), day=int(m.group(3)), 
                hour=int(m.group(4)), minute=int(m.group(5)), second=int(m.group(6))).timetuple())
    return None

import exifread as ef
def gps_info_verified(file, json):
    image_gps_info = []
    with open(image_file, 'rb') as f:
        tags = ef.process_file(f)
        print("GPSLatitude", tags.get('GPS GPSLatitude'))
    return False

def get_exif_datetime(image_file):
    if 1:
        cmd = ['exiftool', '-d', '"%s"', '-DateTimeOriginal', '-S', '-s', image_file]
        result = subprocess.run(cmd, stdout=subprocess.PIPE)
        print (result.stdout)
        return result.stdout
    timestamps = []
    with open(image_file, 'rb') as f:
        image = Image(f)
        if image:
            info_dir = dir(image)
            if image.has_exif:
                for dt in ( 'datetime_digitized', 'datetime_original', 'datetime',):
                    if dt in info_dir:
                        val = getattr(image, dt)
                        try:
                            val = str2timestamp(val)
                        except:
                            print(val, "problem parsing time")
                            input() 
                            val = None
                        if val:
                            timestamps.append(val)
    if timestamps == []:
        return None
    return min(timestamps)
import json
def get_json_timestamp(json_file):
    with open(json_file, "r") as f:
        timestamps = []
        meta = json.load(f)
        for name in ("photoTakenTime", "creationTime"):
            if name in meta.keys():
                if "timestamp" in meta[name].keys():
                    timestamps.append(int(meta[name]["timestamp"]))
    if timestamps == []:
        return None
    return min(timestamps)               
def json_has_gps_info(json_file):
    with open(json_file, "r") as f:
        meta = json.load(f)
        for data in ("geoData", "geoDataExif"):
            if data in meta.keys():
                for name in ("latitude", "longitude", "altitude"):
                    if name in meta[data].keys():
                        value = float(meta[data][name])
                        if value != 0.0:
                            return True
                        print(name, value)
    return False
      

import datetime
import subprocess

class DateNotFoundException(Exception):
    pass

def get_photo_date_taken(filepath):
    """Gets the date taken for a photo through a shell."""
    cmd = "mdls '%s'" % filepath
    output = subprocess.check_output(cmd, shell = True)
    lines = output.decode("ascii").split("\n")
    for l in lines:
        if "kMDItemContentCreationDate" in l:
            datetime_str = l.split("= ")[1]
            return datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S +0000")
    raise DateNotFoundException("No EXIF date taken found for file %s" % filepath)

class archive():
    def __init__(self, archive_path):
        self.archive_path = archive_path
    
    def copy_jpeg_with_exif_datetime_without_json(self, folder):
        files = Files(folder, ("jpg","JPG", "jpeg", "JPEG"))
        count = 0
        for (file, json) in files.next_file():
            #print(file)
            dest = Path(self.archive_path, "no_date")
            try:
                ctime = get_exif_datetime(file)
                    
            except:
                ctime = None

            if not ctime:
                if json:
                    ctime = get_json_timestamp(json)
            if ctime:
                d = time.localtime(ctime)
                if json_has_gps_info(json):
                    dest =  Path(self.archive_path, "dated_with_json", str(d.tm_year), str(d.tm_mon), str(d.tm_mday))
                else:
                    dest =  Path(self.archive_path, "dated", str(d.tm_year), str(d.tm_mon), str(d.tm_mday))

            f = smart_copy(
                file, 
                dest, 
                #src_folder= folder, 
                new_suffix="jpg",
                flush = True,
                delete_original=True,
                ctime=ctime)
            #print (f.get_dst())
            if json and json_has_gps_info(json):
                merge_cmd = 'exiftool -r -d %s -tagsfromfile {}'.format(json)
                merge_cmd = merge_cmd + ' -GPSAltitude<GeoDataAltitude' 
                merge_cmd = merge_cmd + ' -GPSLatitude<GeoDataLatitude'
                merge_cmd = merge_cmd + ' -GPSLatitudeRef<GeoDataLatitude'
                merge_cmd = merge_cmd + ' -GPSLongitude<GeoDataLongitude'
                merge_cmd = merge_cmd + ' -GPSLongitudeRef<GeoDataLongitude' 
                merge_cmd = merge_cmd + ' -Keywords<Tags'
                merge_cmd = merge_cmd + ' -Subject<Tags' 
                merge_cmd = merge_cmd + ' -Caption-Abstract<Description'
                merge_cmd = merge_cmd + ' -ImageDescription<Description' 
                merge_cmd = merge_cmd + ' -ext jpg -overwrite_original'
                merge_cmd = merge_cmd + " " + f.get_dst()

                print(merge_cmd)
                if not gps_info_verified(f.get_dst(), json):
                    print("Preserving json as the gps info seems incorrect")
                    smart_copy(json, 
                    f.get_dst() + ".json", 
                    flush = True,
                    ctime=ctime)
                
            elif json:
                print("json not copied as no gps info found")
            if json:
                os.remove(json)
            
    def copy_non_photo_images(self, folder, extensions, sub_folder):
        
        files = Files(folder, extensions)
        count = 0
        for (file, json) in files.next_file():
            if not json:
                f = smart_copy(
                    file, 
                    Path(self.archive_path, sub_folder), 
                    new_suffix=extensions[0],
                    flush = True,
                    delete_original=True)
                print (f.get_dst())
                    
if __name__ == "__main__":
    a = archive('/Volumes/BlackDiskBackup/Photos')
    a.copy_jpeg_with_exif_datetime_without_json('/Volumes/BlackDiskBackup/Photos/dated_with_json2')
    #a.copy_non_photo_images('/Volumes/BlackDiskBackup/Collection', ("png", "PNG"), "png")
    #a.copy_non_photo_images('/Volumes/BlackDiskBackup/Collection', ("gif", "GIF"), "gif")
    #a.copy_non_photo_images('/Volumes/BlackDiskBackup/Collection', ("bmp", "BMP"), "bmp")
    #a.copy_non_photo_images('/Volumes/BlackDiskBackup/Collection', ("tif", "TIF"), "tif")

   
    
    
"""

    def get_json(self, filepath):
        json_file = Path(filepath + ".json")
        if Path(json_file).exists():
            return json_file
        # handle scenario where fname(N).ext ==> fname.ext(N).json (MAC specfic ??)
        file = Path(filepath)
        p = re.compile('(.*\\s*)(\(\d+\\))\.(.*)$')
        m = p.match(file.name)
        if m:
            json_file = Path(file.parent, "{}.{}{}.json".format(
                m.group(1), m.group(3), m.group(2)))
            if Path(json_file).exists():
                return json_file
        return None

from exif import Image
def get_exif_datetime(file):
    timestamps = []
    with open(image_file, 'rb') as f:
        image = Image(f)
        if image:
            info_dir = dir(image)
            if image.has_exif:
                for dt in ( 'datetime_digitized', 'datetime_original', 'datetime',):
                    if dt in info_dir:
                        val = getattr(image, dt)
                        val = self.str2timestamp(val)
                        if val:
                            timestamps.append(val)
    if timestamps == []:
        return None
    return min(timestamps)

class arcive():
    def __init__(self, archive_path):
        self.archive_path = archive_path
    
    def copy_jpeg_with_exif_datetime_without_json(self, folder, extensions):
        files = Files(folder, ("jpg","JPG", "jpeg", "JPEG"))
        for (file, json) in files.next_file():
            if not json:
                ctime = get_exif_datetime(file)
                if ctime:
                    smart_copy(
                        file, 
                        Path(self.archive_path, "no_json", "ctime_found"), 
                        src_folder= folder, 
                        new_suffix="jpg",
                        flush = False,
                        delete_original=True,
                        ctime= ctime)

if __name__ == "__main__":
    a = arcive('/Volumes/WhiteDisk202001/Photos')
    a.copy_jpeg_with_exif_datetime_without_json('/Volumes/WhiteDisk202001/AkilanArchive/Takeout/Google Photos', )


file_counter = [0, 0]
for subdir, dirs, files in os.walk(args.folder):
    for filename in files:
        filepath = subdir + os.sep + filename
        json_end_string = ".json"
        if filepath.endswith(json_end_string):
            # Fix up the name




            print(filepath)
            base_filepath = filepath.rstrip(json_end_string)
            if not os.path.exists(base_filepath):
                print(base_filepath, " not found")
                os.remove(filepath)
                print("deleted")
                file_counter[0] = file_counter[0] + 1
            if not json_has_gps_info(filepath):
                os.remove(filepath)
                print("deleted")
                file_counter[1] = file_counter[1] + 1
print(file_counter)

"""