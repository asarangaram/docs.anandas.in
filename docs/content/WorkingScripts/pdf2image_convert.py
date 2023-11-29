#!/usr/bin/env python3
import os
import pdf2image
from pathlib import Path
def convert(file):
    f = Path(file)
    output_folder = Path(f.parent, f.stem)
    if not os.path.exists(output_folder):
        os.mkdir(output_folder)
    pdf2image.convert_from_path(
        f, fmt="jpeg",
        output_folder=output_folder,
        thread_count=10,
        output_file=f.stem + " ")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="the file that should be processed")
    args = parser.parse_args()
    convert(args.file)
