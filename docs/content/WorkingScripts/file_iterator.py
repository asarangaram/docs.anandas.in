#!/usr/bin/env python3
import os


class Files():
    def __init__(self, folder, extensions):
        self.folder = folder
        self.extensions = extensions
        self.counter = 0

    def next_file(self):
        for extension in self.extensions:
            for subdir, dirs, files in os.walk(self.folder):
                for filename in files:
                    filepath = subdir + os.sep + filename
                    if filepath.endswith(extension):
                        self.counter = 0
                        yield (filepath)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("folder", help="the folder that should be processed")
    args = parser.parse_args()
    _ = Files(args.folder, ("json", ))
    for file in _.next_file():
        print (file)