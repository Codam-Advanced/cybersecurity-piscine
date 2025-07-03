import argparse
import sys
from PIL import Image, ExifTags

def extract_file_data(files: list[str]):
    for file in files:
        image = Image.open(file)
        exif_data = image.getexif().items()

        print("\n\n+" + "-"*70 + "+")
        print("|{:^70}|".format(f"The Image - [{image.filename}]"))
        print("+" + "-"*70 + "+")
        print((f"| The Image Format	    - [{image.format}]").ljust(50) + "|")
        print((f"| The Image Size	    - W [{image.width}] H [{image.height}]").ljust(48) + "|")

        for key, val in exif_data:
            if ExifTags.TAGS[key] != "DateTime":
                        continue
            print((f"| The Image Creation date   - [{val}]").ljust(55) + "|")

        print("\n[EXIF_DATA]:")
        if not exif_data:
            print("Sorry, image has no exif data.")
        else:
            for key, val in exif_data:
                if key in ExifTags.TAGS:
                    if ExifTags.TAGS[key] == "DateTime":
                        continue
                    print(f"[{ExifTags.TAGS[key]}]:({val})")
                else:
                    print(f"[{key}]:({val})")         

if "__main__" == __name__:
    parser = argparse.ArgumentParser()
    parser.add_argument("Files", type=str, nargs="+", help="The files to be analyzed")
    args = parser.parse_args()

    for file in args.Files:
        if (file.endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp"), 1) == False):
            sys.exit("Error: File needs to have an image extension (.jpg, .jpeg, .png, .gif, .bmp)")
    extract_file_data(args.Files)
