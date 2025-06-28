import argparse
import sys
from PIL import Image


def extract_file_data(files: list[str]):
    for file in files:
        print(file)
        image = (Image.open(file))
        exif_data = image.getexif()
        print(exif_data.pop())        
                

if "__main__" == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument("Files", type=str, nargs="+", help="The files to be analyzed")
    args = parser.parse_args()

    for file in args.Files:
        if (file.endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp"), 1) == False):
            sys.exit("Error: File needs to have an image extension (.jpg, .jpeg, .png, .gif, .bmp)")
    extract_file_data(args.Files)