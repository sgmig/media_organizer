import os
import shutil
import re
from PIL import Image
from datetime import datetime
import argparse


# reading taken date from exif data
def _get_date_taken_from_exif(file):
    # returs a string with the date taken
    exif = Image.open(file)._getexif()
    if not exif:
        # raise Exception(f"Image {filename} does not have EXIF data.")
        return None
    exif_datetime_str = exif.get(36867)
    if not exif_datetime_str:
        return None
    exif_datetime = datetime.strptime(exif_datetime_str, "%Y:%m:%d %H:%M:%S")
    return exif_datetime


def _get_last_mod_date(file):
    secs_from_epoch = os.path.getmtime(file)
    if secs_from_epoch:
        last_mod_date = datetime.fromtimestamp(secs_from_epoch)

        return last_mod_date
    else:
        return None


def _get_date_from_name(file):

    filename, _ = os.path.splitext(file)

    date_re = "\D(20\d{6}(?:[_-]?[012]\d[0-5]\d(?:[0-5]\d)?)?)\D"
    date_re_match = re.findall(date_re, filename)
    # if the list is not empty, we have found something
    if date_re_match:
        date_found = date_re_match[0]
        date_found = date_found.replace("-", "_")
        date_format = "%Y%m%d"
        if "_" in date_found:
            date_format += "_"

        date_len = len(date_found)
        if date_len > 8:
            date_format += "%H%M"
            if date_len > 10:
                date_format += "%S"

        date_from_filename = datetime.strptime(date_found, date_format)
        return date_from_filename
    else:
        return None


def get_date(file):
    # call different functions to get the date we'll assign to the picture.

    # first attempt, we get the taken date from the exif data. This is the best case scenario.

    date = _get_date_taken_from_exif(file)

    if date:
        # print("EXIF")
        return date
    # second attempt, we get from the filename. This works for my cellphone pictures.
    date = _get_date_from_name(file)
    if date:
        # print("NAME")
        return date

    date = _get_last_mod_date(file)
    if date:
        # print("MOD_DATE")
        return date
    else:
        return None


def organize_pictures_by_date(source_folder, destination_folder, mode="move"):

    copy_function = shutil.copy if mode == "copy" else shutil.move

    for dirname, subdirs, files in os.walk(source_folder):
        for file in files:
            filename, file_ext = os.path.splitext(file)
            print(filename)
            is_jpeg = bool(re.search("\\.jpe?g$", file_ext, re.IGNORECASE))
            if is_jpeg:
                # Now we try to access the date taken attribute.
                # datetime object. This fuinction will try a few methods
                # to return a datetime object from the picture.
                source_file_path = os.path.join(dirname, file)
                date_taken = get_date(source_file_path)

                if date_taken:
                    # create the directory with format YYYYMM
                    destination_folder_by_date = os.path.join(
                        destination_folder, f"{date_taken.strftime('%Y%m')}"
                    )

                    if not os.path.exists(destination_folder_by_date):
                        os.makedirs(destination_folder_by_date)

                    i = 0
                    while True:
                        index_string = f"_{i}" if i else ""
                        new_filename = os.path.join(
                            destination_folder_by_date,
                            date_taken.strftime("%Y%m%d_%H%M%S")
                            + index_string
                            + ".jpg",
                        )

                        # if the name does not exist, we copy. If it does, we add try adding and index
                        # until we find an available filename.
                        if not os.path.exists(new_filename):
                            print(f"--> {new_filename}")
                            copy_function(
                                source_file_path,
                                new_filename,
                            )
                            break
                        i += 1


# let's try first to read the filenames (for the whatsapp use case)
# Apparently for whatsapp files I can use date modifiied.
# So we'll try to access date created, if not there, we go to date modified.

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Organize JPG files by date.")
    parser.add_argument("source", help="Source folder containing JPG files")
    parser.add_argument("destination", help="Destination folder to organize files into")
    parser.add_argument(
        "--mode",
        choices=["move", "copy"],
        default="move",
        help="Whether to move or copy the files (default: move)",
    )
    args = parser.parse_args()

    organize_pictures_by_date(args.source, args.destination, args.mode)
