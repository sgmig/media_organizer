# Organize Pictures by Date

This script organizes JPG files into folders based on their creation date. It uses metadata from EXIF data, filenames, or file modification dates to determine the date and organize the files accordingly.

## Features

- Extracts dates from EXIF data, filenames, or file modification dates.
- Supports moving or copying files.
- Organizes files into folders named by year and month (e.g., `202501` for January 2025).
- Handles duplicate filenames gracefully by appending an index to the new filename.

## Prerequisites

1. Python 3.x
2. Required packages:
   - `Pillow`
   - `argparse`

Install the dependencies using:
```bash
pip install pillow
```

## Usage

Run the script from the command line:
```bash
python organize_pictures.py <source_folder> <destination_folder> [--mode move|copy]
```

### Arguments
- `source_folder`: The folder containing the JPG files to organize.
- `destination_folder`: The folder where the organized files will be saved.
- `--mode`: Optional. Specifies whether to `move` or `copy` the files. Default is `move`.

### Examples

1. **Move files**:
   ```bash
   python organize_pictures.py ./Pictures ./Organized
   ```

2. **Copy files instead of moving**:
   ```bash
   python organize_pictures.py ./Pictures ./Organized --mode copy
   ```

## Notes

- The script processes only `.jpg` or `.jpeg` files.
- If EXIF data is unavailable, it falls back to dates in filenames or the last modified date.
- Ensure you have read/write permissions for the specified folders.
