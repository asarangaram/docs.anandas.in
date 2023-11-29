#!/usr/local/bin/python3

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
import subprocess
from smart_copy import smart_copy

video_extensions = (".mov", ".avi", ".mp4",".MOV", ".AVI", ".MP4", ".m4v", ".3gp")
def is_video(file):
    f = Path(file)
    if f.suffix in video_extensions:
        #print (file, "is Video")
        return True
    return False
photo_extensions = (".HEIC", ".heic", ".jpg", ".JPG", ".jpeg", ".JPEG")
def is_photo(file):
    f = Path(file)
    if f.suffix in photo_extensions:
        #print (file, "is Image")
        return True
    return False

def valid_time(yyyy, mm, dd, HH="0", MM="0", SS = "0"):
    dt = None
    try:
        dt = datetime.datetime(int(yyyy)+2000, int(mm), int(dd), int(HH), int(MM), int(SS), 0)
    except:
        dt = None
    if dt:
        return True
    return False

def convert2timestamp(yyyy, mm, dd, HH="0", MM="0", SS = "0"):
    print(int(yyyy), int(mm), int(dd), int(HH), int(MM), int(SS))
    if int(yyyy) < 100:
        dt = datetime.datetime(int(yyyy)+2000, int(mm), int(dd), int(HH), int(MM), int(SS), 0)
    else:
        dt = datetime.datetime(int(yyyy), int(mm), int(dd), int(HH), int(MM), int(SS), 0)
    return (time.mktime(dt.timetuple()))


def exif_parse_table(image_file):
    
    p = re.compile('\"(\d+)\"\n?')
    cmd = ['exiftool', '-d', '"%s"', image_file]
    result = subprocess.run(cmd, stdout=subprocess.PIPE)

    output = result.stdout.decode('latin-1').split("\n")
    d = {}
    for item in output:
        if item:
            info_pair = item.split(":")
            if info_pair:
                d[info_pair[0].strip()] = info_pair[1].strip()
    #print(json.dumps(d))
    if "Create Date" in d.keys():
        m = p.match(d["Create Date"])
        if m:
            return int(m.group(1))  
    if "Media Create Date" in d.keys():
        m = p.match(d["Media Create Date"])
        if m:
            return int(m.group(1)) 
    if "Modify Date" in d.keys():
        m = p.match(d["Modify Date"])
        if m:
            return int(m.group(1))
    if "Photo Taken Time Timestamp" in d.keys():
        m = p.match(d["Photo Taken Time Timestamp"])
        if m:
            return int(m.group(1))
    if "Creation Time Timestamp" in d.keys():
        m = p.match(d["Creation Time Timestamp"])
        if m:
            return int(m.group(1))
    
    file = Path(image_file)
    stem = file.stem
    parent_stem = file.parent.stem
    print(parent_stem, " / ", stem)

    p1 = re.compile("IMG\-(\d\d\d\d)(\d\d)(\d\d)\-WA.*$")
    match = p1.match(stem)
    if match:
        (y, m, d) = (match.group(1), match.group(2),match.group(3))
        (H, M, S) = (0, 0, 0)
        if (valid_time(y, m, d, HH=H, MM=M, SS=S)):
            return convert2timestamp(y, m, d, HH=H, MM=M, SS=S)
    p1 = re.compile("VID\-(\d\d\d\d)(\d\d)(\d\d)\-WA.*$")
    match = p1.match(stem)
    if match:
        (y, m, d) = (match.group(1), match.group(2),match.group(3))
        (H, M, S) = (0, 0, 0)
        if (valid_time(y, m, d, HH=H, MM=M, SS=S)):
            return convert2timestamp(y, m, d, HH=H, MM=M, SS=S)

    p2 = re.compile("4-up\ on\ (\d+)\-(\d+)\-(\d+)\ at\ (\d+)\.(\d+).*")
    match = p2.match(stem)
    if match:
        (y, m, d) = (match.group(3), match.group(2),match.group(1))
        (H, M, S) = (match.group(4), match.group(5), 0)
        if (valid_time(y, m, d, HH=H, MM=M, SS=S)):
            return convert2timestamp(y, m, d, HH=H, MM=M, SS=S)
    p3 = re.compile("^Screenshot_(\d\d\d\d)(\d\d)(\d\d)-(\d\d)(\d\d)(\d\d).*")
    match = p3.match(stem)
    if match:
        (y, m, d) = (match.group(1), match.group(2),match.group(3))
        (H, M, S) = (match.group(4), match.group(5), match.group(6))
        if (valid_time(y, m, d, HH=H, MM=M, SS=S)):
            return convert2timestamp(y, m, d, HH=H, MM=M, SS=S)
    p4 = re.compile(".*[^0-9]([0-9]{8})[^0-9]?([0-9]{6})([^0-9].*$|$)")
    match = p4.match(stem)
    if match:
        ymd = match.group(1)
        HMS = match.group(2)
        
        (y, m, d) = (ymd[0:4], ymd[4:6],ymd[6:8])
        (H,M,S)   = (HMS[0:2], HMS[2:4],HMS[4:6])
        if (valid_time(y, m, d, HH=H, MM=M, SS=S)):
            return convert2timestamp(y, m, d, HH=H, MM=M, SS=S)
    p5 = re.compile(".*[^0-9]([0-9]{8})[^0-9]?([0-9]{2})[\-_]([0-9]{2})[\-_]([0-9]{2})([^0-9].*$|$)")
    match = p5.match(stem)
    if match:
        ymd = match.group(1)
        H = match.group(2)
        M = match.group(3)
        S = match.group(4)
        (y, m, d) = (ymd[0:4], ymd[4:6],ymd[6:8])
        if (valid_time(y, m, d, HH=H, MM=M, SS=S)):
            return convert2timestamp(y, m, d, HH=H, MM=M, SS=S)
    """
    p6 = re.compile(".*(\d{2})\-(\d{2})\-(\d{2})\sat\s(\d{2})\.(\d{2})\s?(AM|PM)?($|[^0-9].*$)")
    match = p6.match(stem)
    if match:
        d = match.group(1)
        m = match.group(2)
        y = match.group(3)
        is_pm = match.group(6) == 'PM'
        H = match.group(4) if not is_pm else int(match.group(4)) + 12 
        M = match.group(5)
        
        return convert2timestamp(y, m, d, HH=H, MM=M, SS=0)
                    
    p7 = re.compile(".*(\d{2})\-(\d{2})\-(\d{2})\sat\s(\d{2})\.(\d{2})\.(\d{2})\s?(AM|PM)?($|[^0-9].*$)")
    match = p7.match(stem)
    if match:
        d = match.group(1)
        m = match.group(2)
        y = match.group(3)
        is_pm = match.group(7) == 'PM'
        H = match.group(4) if not is_pm else int(match.group(4)) + 12 
        M = match.group(5)
        S = match.group(6)
        
        return convert2timestamp(y, m, d, HH=H, MM=M, SS=S)

    p8 = re.compile(".*(\d{4})\-(\d{2})\-(\d{2})\sat\s(\d{2})\.(\d{2})\s?(AM|PM)($|[^0-9].*$)")
    match = p8.match(stem)
    if match:
        d = match.group(1)
        m = match.group(2)
        y = match.group(3)
        is_pm = match.group(6) == 'PM'
        H = match.group(4) if not is_pm else int(match.group(4)) + 12 
        M = match.group(5)
        
        return convert2timestamp(y, m, d, HH=H, MM=M, SS=0)
                    
    p9 = re.compile(".*(\d{4})\-(\d{2})\-(\d{2})\sat\s(\d{2})\.(\d{2})\.(\d{2})\s?(AM|PM)($|[^0-9].*$)")
    match = p9.match(stem)
    if match:
        y = match.group(1)
        m = match.group(2)
        d = match.group(3)
        is_pm = match.group(7) == 'PM'
        H = match.group(4) if not is_pm else int(match.group(4)) + 12 
        M = match.group(5)
        S = match.group(6)
            
        return convert2timestamp(y, m, d, HH=H, MM=M, SS=S)
    """
    P1 = re.compile("^(\d\d\d\d)\-(\d\d)\-(\d\d)($|[^0-9].*$)")
    match = P1.match(parent_stem)
    
    if match:
        (y, m, d) = (match.group(1), match.group(2),match.group(3))
        (H, M, S) = (0, 0, 0)
        return convert2timestamp(y, m, d, HH=H, MM=M, SS=S)
    
    return None

def get_exif_datetime(image_file):
    p = re.compile('\"(\d+)\"\n?')
    if 1:
        cmd = None
        if is_video(image_file):
           return exif_parse_table(image_file) 
  
        elif is_photo(image_file):
            cmd = ['exiftool', '-d', '"%s"', '-DateTimeOriginal', '-S', '-s', image_file]
            result = subprocess.run(cmd, stdout=subprocess.PIPE)
            ts = result.stdout.decode("utf-8") 
            m = p.match(ts)
            if m:
                return int(m.group(1))   
            else:
                return exif_parse_table(image_file)
            
    return None
     
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="the folder that should be processed")
    args = parser.parse_args()
    unexpected_extensions = ("jpg_original", "mp4_original", "JPG_original","jpeg_original",
     "GIF_original", "tiff_original", "gif_original", "HEIC_original", "MOV_original", "PNG_original", "mov_original", "png_original")
    if 0:
        _ = Files(args.folder, (unexpected_extensions))
        for file in _.next_file():
            f_original = Path(file)
            f = Path(f_original.parent, f_original.stem + f_original.suffix.replace("_original", ""))
            
            if os.path.exists(f):
                print(f, " -> ", Path(f.parent, f.stem + "_copy" + f.suffix))
                os.rename(f, Path(f.parent, f.stem + "_copy" + f.suffix))
            print(file, " -> ", f)
            os.rename(file, f)
        exit (0)
    if 1:
        _ = Files(args.folder, photo_extensions)
        #print (args.folder)
        file_count = 0
        progress = report_progress_basic()

        for file in _.next_file():
            ctime = get_exif_datetime(file)
            if not ctime:
                
                dest =  Path("/Volumes/BlackDiskBackup/no_date_photos")
            else:
                d = time.localtime(ctime)
                #print(d)
                dest =  Path("/Volumes/BlackDiskBackup/OrganizedPhotos", str(d.tm_year), str(d.tm_mon), str(d.tm_mday))
            f = smart_copy(
                file, 
                dest, 
                flush = True,
                #new_suffix="jpg",
                delete_original=True,
                ctime=ctime)
            progress.update(lap_after=100)
    if 1:
        _ = Files(args.folder, video_extensions)
        #print (args.folder)
        file_count = 0
        progress = report_progress_basic()

        for file in _.next_file():
            ctime = get_exif_datetime(file)
            if not ctime:
                
                dest =  Path("/Volumes/BlackDiskBackup/no_date_videos")
            else:
                d = time.localtime(ctime)
                #print(d)
                dest =  Path("/Volumes/BlackDiskBackup/OrganizedVideos", str(d.tm_year), str(d.tm_mon), str(d.tm_mday))
            f = smart_copy(
                file, 
                dest, 
                flush = True,
                delete_original=True,
                ctime=ctime)
            progress.update(lap_after=100)
    if 1:
        dest =  Path("/Volumes/BlackDiskBackup/images")
        image_extensions = (".gif", ".GIF", ".png", ".PNG", ".tiff", ".bmp", ".BMP")
        _ = Files(args.folder, image_extensions)
        for file in _.next_file():
            f = smart_copy(
            file, 
            dest, 
            flush = True,
            delete_original=True)
    if 1:
        dest =  Path("/Volumes/BlackDiskBackup/audio")
        image_extensions = (".mp3", ".opus", )
        _ = Files(args.folder, image_extensions)
        for file in _.next_file():
            f = smart_copy(
            file, 
            dest, 
            flush = True,
            delete_original=True)
    if 1:
        dest =  Path("/Volumes/BlackDiskBackup/documents")
        image_extensions = (".pdf", ".docx", ".PDF")
        _ = Files(args.folder, image_extensions)
        for file in _.next_file():
            f = smart_copy(
            file, 
            dest, 
            flush = True,
            delete_original=True)