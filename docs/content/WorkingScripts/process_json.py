#!/usr/bin/env python3
from pathlib import Path
import re
import os
import argparse
import json

from file_iterator import Files
from report_progress import report_progress_basic
from exif import Image
import re
import calendar
import datetime
import time

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


def str2timestamp(val):
    if val != '0000:00:00 00:00:00':
        p = re.compile('(.*):(.*):(.*)\ (.*):(.*):(.*)')
        m = p.match(val)
        if m:
            return time.mktime(datetime.datetime(
                year=int(m.group(1)), month=int(m.group(2)), day=int(m.group(3)), 
                hour=int(m.group(4)), minute=int(m.group(5)), second=int(m.group(6))).timetuple())
    return None

def get_exif_datetime(image_file):
    timestamps = []
    with open(image_file, 'rb') as f:
        image = Image(f)
        if image:
            info_dir = dir(image)
            if image.has_exif:
                for dt in ('datetime_digitized', 'datetime_original', 'datetime',):
                    if dt in info_dir:
                        
                        try:
                            val = getattr(image, dt)
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


def merge_json(folder):
    merge_cmd = "exiftool -r -d %s -tagsfromfile \"%d/%F.json\" " \
        "\"-GPSAltitude<GeoDataAltitude\" \"-GPSLatitude<GeoDataLatitude\" " \
        "\"-GPSLatitudeRef<GeoDataLatitude\" \"-GPSLongitude<GeoDataLongitude\" " \
        "\"-GPSLongitudeRef<GeoDataLongitude\" \"-Keywords<Tags\" " \
        "\"-Subject<Tags\" \"-Caption-Abstract<Description\" " \
        "\"-ImageDescription<Description\" \"-DateTimeOriginal<PhotoTakenTimeTimestamp\"" \
        "-overwrite_original "
    
    print(merge_cmd + folder)
    retVal = os.system(merge_cmd + folder)
    return retVal


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="the folder that should be processed")
    args = parser.parse_args()
    if 1:
        _ = Files(args.folder, ("json", ))
        file_count = 0
        for file in _.next_file():
            candidate = Path(file)
            p = re.compile('(.*)\.(.*)(\(.*\))\.json$')
            m = p.match(candidate.name)
            if m:
                new_name = "{}{}.{}.json".format( m.group(1), m.group(3), m.group(2))
                new_candidate = Path(candidate.parent, new_name)
                print ("Moving ", candidate, " -> ", new_candidate)
                os.rename(candidate, new_candidate)
                candidate = Path(file)
            content_file = Path(str(candidate).rstrip(".json"))
            if not os.path.exists(content_file):
                print("Removing Stale ", candidate)
                os.remove(candidate)
                file_count = file_count +1
        print("file_count = ", file_count)
    if 0:
         merge_json(args.folder)
    if 0:
        _ = Files(args.folder, ("json", ))
        file_count = 0
        progress = report_progress_basic()
        for file in _.next_file():
            candidate = Path(file)
            content_file = Path(str(candidate).rstrip(".json"))
            print(content_file, flush=True)
            UnSupportedTypes = (".png", ".gif", ".PNG", ".GIF")
            print("suffix ", content_file.suffix)
            ts1 = None
            #if not content_file.suffix in UnSupportedTypes:
            #    ts1 = get_exif_datetime(content_file)
            
            if not ts1:
                merge_cmd = "exiftool -r -d %s -tagsfromfile \"%d/%F.json\" " \
                    "\"-GPSAltitude<GeoDataAltitude\" \"-GPSLatitude<GeoDataLatitude\" " \
                    "\"-GPSLatitudeRef<GeoDataLatitude\" \"-GPSLongitude<GeoDataLongitude\" " \
                    "\"-GPSLongitudeRef<GeoDataLongitude\" \"-Keywords<Tags\" " \
                    "\"-Subject<Tags\" \"-Caption-Abstract<Description\" " \
                    "\"-ImageDescription<Description\" \"-DateTimeOriginal<PhotoTakenTimeTimestamp\"" \
                    " -overwrite_original "
            else:
                merge_cmd = "exiftool -r -d %s -tagsfromfile \"%d/%F.json\" " \
                    "\"-GPSAltitude<GeoDataAltitude\" \"-GPSLatitude<GeoDataLatitude\" " \
                    "\"-GPSLatitudeRef<GeoDataLatitude\" \"-GPSLongitude<GeoDataLongitude\" " \
                    "\"-GPSLongitudeRef<GeoDataLongitude\" \"-Keywords<Tags\" " \
                    "\"-Subject<Tags\" \"-Caption-Abstract<Description\" " \
                    "\"-ImageDescription<Description\" " \
                    " -overwrite_original "
            print(merge_cmd + "'{}'".format(str(content_file)))
            retVal = os.system(merge_cmd + "'{}'".format(str(content_file)))
            progress.update(lap_after=2000)
        progress.lap()
