#!/usr/bin/env python3

import os
from pathlib import Path
import shutil
import time
import datetime
class smart_copy():
    def __init__(self, src, dst,
                 src_folder=None,
                 new_suffix=None,
                 overwrite = False,
                 flush=True,
                 delete_original=False,
                 ctime=None):
        """
            src : file that to be copied.
            dst: file or destination folder.
            src_folder: parent folder to identify the subfolders in src
            new_suffix: new suffix if suffix change is required.
            flush: to perform actual copy or wait for actual copy.
            FIXME: 
            * Have smart_copy
            * Implement across drives
        """
        self.src = Path(src)
        self.delete_original = delete_original
        self.ctime = ctime
        dst = Path(dst)
        if src_folder:
            src_folder = Path(src_folder)
        if  new_suffix:
            new_suffix = new_suffix if new_suffix[0] == '.' else "." + new_suffix
        
        self.dst = self.get_dst_fname(self.src, dst, src_folder, new_suffix)
        
        if not overwrite:
            incr = 0
            while os.path.exists(self.dst):
                #print("looop")
                #print(self.dst)
               
                incr = incr + 1
                self.dst = self.get_dst_fname(self.src, dst, src_folder, new_suffix, incr=incr)
       
        print (" Copying {} -> {} : {}".format( self.src, self.dst, "dry_run" if not flush else "done"))
        if flush:
            self.copy(delete_original = self.delete_original)

    def copy(self, delete_original=False):
        if not os.path.exists(self.src):
            raise IOError (str(self.src) + " Not found")
        if not os.path.exists(self.dst.parent):
            os.makedirs(self.dst.parent) 
        if not self.src == self.dst:
            shutil.copy2(self.src, self.dst)
        if delete_original:
            os.remove(self.src)
        if self.ctime:
            date = datetime.datetime.fromtimestamp(self.ctime)
            
            os.system ('touch -t "{}" "{}"'.format(date.strftime('%Y%m%d%H%M.%S'), self.dst))
            os.system ('SetFile -d "{}" "{}"'.format(date.strftime('%m/%d/%Y %H:%M:%S'), self.dst))
            #os.system ('SetFile -m "{}" {}'.format(date.strftime('%m/%d/%Y %H:%M:%S'), self.dst))
            #os.utime(self.dst, (self.ctime, self.ctime))
            stat = os.stat(self.dst)
            #print("atime : ", time.asctime( time.localtime(stat.st_atime)))
            #print("ctime : ", time.asctime( time.localtime(stat.st_ctime)))
            #print("mtime : ", time.asctime( time.localtime(stat.st_mtime)))


    def get_dst(self):
        return str(self.dst)

    def get_dst_fname(self, src, dst, src_folder, new_suffix, incr = None):  
        dir = False
        
        if not os.path.exists(dst):
            if dst.suffix == "":
                dir = True
        else:
            if os.path.isdir(dst):
                dir = True
        
        if dir:   
            sub_folders = None
            if src_folder:
                sub_folders = Path(src).relative_to(Path(src_folder))
                if str(sub_folders) == str(src):
                    sub_folders = None
            if sub_folders:
                sub_folders = sub_folders.parent
            
            if new_suffix:
                suffix = new_suffix
            else:
                suffix = src.suffix
            
            tmp = "({})".format(incr) if incr else ""
            suffix = tmp + suffix
            dst = Path(
                dst,
                sub_folders if sub_folders else Path(""), 
                src.stem + suffix) 
            
        else:
            parent = dst.parent
            stem = dst.stem
            suffix = dst.suffix
            
            
            tmp = "({})".format(incr) if incr else ""
            suffix = tmp + suffix
            dst = Path(
                parent,
                stem + suffix) 
           
        if dst.suffix == None:
            print("Suffix missing !!!!")
            exit(-1)
        return dst

if __name__ == "__main__":
    def main():
        m = smart_copy("test_data/src/fldr1/fldr2/fldr3/fldr4/testfile.abc", "test_data/dst/fldr1/fldr2/fldr3/fldr4/test1/testfile.abc"); 
        if not str(m.get_dst()) == "test_data/dst/fldr1/fldr2/fldr3/fldr4/test1/testfile.abc":
            print("test 1 failed")
            print(m.get_dst())
        else:
            print("test 1 pass")
        m = smart_copy("test_data/src/fldr1/fldr2/fldr3/fldr4/testfile.abc", "test_data/dst/fldr1/fldr2/fldr3/fldr4/test2/testfile.def");  
        if not m.get_dst() == "test_data/dst/fldr1/fldr2/fldr3/fldr4/test2/testfile.def":
            print("test 2 failed")
            print(m.get_dst())
        else:
            print("test 2 pass")
        m = smart_copy("test_data/src/fldr1/fldr2/fldr3/fldr4/testfile.abc", "test_data/dst/fldr1/fldr2/fldr3/fldr4/test3"); 
        if not m.get_dst() == "test_data/dst/fldr1/fldr2/fldr3/fldr4/test3/testfile.abc":
            print("test 3 failed")
            print(m.get_dst())
        else:
            print("test 3 pass")
   
        m = smart_copy("test_data/src/fldr1/fldr2/fldr3/fldr4/testfile.abc", "test_data/dst/fldr1/fldr2/fldr3/fldr4/test4", new_suffix="def"); 
        if not m.get_dst() == "test_data/dst/fldr1/fldr2/fldr3/fldr4/test4/testfile.def":
            print("test 4 failed")
            print(m.get_dst())
        else:
            print("test 4 pass")

        m = smart_copy("test_data/src/fldr1/fldr2/fldr3/fldr4/testfile.abc", "test_data/dst/fldr1/fldr2/fldr3/fldr4/test5", src_folder="test_data/src/fldr1/fldr2"); 
        if not m.get_dst() == "test_data/dst/fldr1/fldr2/fldr3/fldr4/test5/fldr3/fldr4/testfile.abc":
            print("test 5 failed")
            print(m.get_dst())
        else:
            print("test 5 pass")
        
        m = smart_copy("test_data/src/fldr1/fldr2/fldr3/fldr4/testfile.abc", "test_data/dst/fldr1/fldr2/fldr3/fldr4/test6", src_folder="test_data/src/fldr1/fldr2/fldr3", new_suffix ="def"); 
        if not m.get_dst() == "test_data/dst/fldr1/fldr2/fldr3/fldr4/test6/fldr4/testfile.def":
            print("test 6 failed")
            print(m.get_dst())
        else:
            print("test 6 pass")


    main()       