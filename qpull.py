#!/usr/bin/env python3

import subprocess
import os
import re
import argparse
import sys

from tqdm import tqdm
import humanize

################################################################################
# START Configuration
# Set the source and destination paths for recordings and screenshots.
# The source path is the directory on the Oculus device.
# The destination path is the directory on your computer.
# The date format is YYYY.MM.DD
# The date format is used to create subdirectories in the destination path.
# The date format is extracted from the filename.
# If the date cannot be extracted, the file is skipped.
# If the date can be extracted, the file is downloaded to the subdirectory.
# If the file is successfully downloaded, it is deleted from the Oculus device.
# If the file cannot be downloaded, it is not deleted from the Oculus device.
# If the --delete flag is used, files are deleted without downloading.
# If the --all flag is used, both recordings and screenshots are processed.
CONFIG = {
    'recordings': {
        'source_path': '/sdcard/Oculus/VideoShots',
        'dest_path': '/Volumes/MBAEXT/GAMING/pulls/screen_recordings'
    },
    'shots': {
        'source_path': '/sdcard/Oculus/Screenshots',
        'dest_path': '/Volumes/MBAEXT/GAMING/pulls/screenshots'
    }
}
# END Configuration
################################################################################
# DO NOT EDIT BELOW THIS LINE
################################################################################

class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        # Custom error message
        sys.stderr.write(f'{message}\n\n')
        # Print help information
        self.print_help()
        # Exit with error status
        sys.exit(2)


def run_command(command):
    """
    Executes a shell command and returns the output as a list of lines.

    Args:
    command (str): The shell command to be executed.

    Returns:
    list: The output of the command split into lines.

    Raises:
    Exception: If the command execution fails.
    """
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        raise Exception(f"Command failed: {result.stderr}")
    return result.stdout.splitlines()

def extract_date(filename):
    """
    Extracts a date from the filename in the format YYYY.MM.DD.

    Args:
    filename (str): The filename from which to extract the date.

    Returns:
    str or None: The extracted date in the format YYYY.MM.DD, or None if the date can't be extracted.
    """
    match = re.search(r'(\d{4})(\d{2})(\d{2})', filename)
    if match:
        return f"{match.group(1)}.{match.group(2)}.{match.group(3)}"
    return None

def get_file_sizes(file_list):
    """
    Parses file sizes from the output of a directory listing.

    Args:
    file_list (list of str): The output lines from a directory listing.

    Returns:
    dict: A dictionary mapping filenames to their sizes in bytes.
    """
    sizes = {}
    for line in file_list:
        parts = line.split()
        if len(parts) > 4:
            try:
                size = int(parts[4])  # Size is the 5th element (index 4)
                file = parts[-1]      # Filename is the last element
                sizes[file] = size
            except ValueError:
                tqdm.write(f"Could not parse size from line: {line}")
    return sizes

def main():
    """
    Main function to handle file pulling from Oculus device.

    This function parses command line arguments for different modes (delete, recordings, shots, all)
    and processes the files accordingly. It handles file listing, downloading, and optional deleting.
    """
    # Parse command line arguments
    parser = CustomArgumentParser(allow_abbrev=False,
                                  description="Pull files from Oculus device and optionally delete them.")
    parser.add_argument('-r', '--recordings', action='store_true', help='Process screen recordings')
    parser.add_argument('-s', '--shots', action='store_true', help='Process screenshots')
    parser.add_argument('-a', '--all', action='store_true', help='Process both recordings and screenshots')
    parser.add_argument('--delete', action='store_true', help='Delete files upon successful download')
    args = parser.parse_args()

    if not (args.recordings or args.shots or args.all):
        parser.print_help()
        return

    tasks = []
    if args.recordings or args.all:
        tasks.append('recordings')
    if args.shots or args.all:
        tasks.append('shots')

    for task in tasks:
        file_list_output = run_command(f"adb shell ls -l {CONFIG[task]['source_path']}")

        file_sizes = get_file_sizes(file_list_output)
        total_size = sum(file_sizes.values())
        total_files = len(file_sizes)

        with tqdm(total=total_size, desc=f"Overall Progress {task} : ", unit="B", unit_scale=True) as overall_progress:
            current_file_number = 0
            for line in file_list_output:
                parts = line.split()
                if len(parts) > 4:
                    file = parts[-1]
                    if file not in file_sizes:
                        tqdm.write(f"Skipping file {file} (size not determined).")
                        continue

                    current_file_number += 1
                    human_readable_size = humanize.naturalsize(file_sizes[file])
                    tqdm.write(f"Downloading: {file} ({human_readable_size})")
                    overall_progress.set_description(f"Overall Progress {task} : (File {current_file_number} of {total_files})")

                    date = extract_date(file)
                    if date:
                        dir_path = os.path.join(CONFIG[task]['dest_path'], date)
                        if not os.path.exists(dir_path):
                            os.makedirs(dir_path)

                        adb_pull_command = f"adb pull {CONFIG[task]['source_path']}/{file} {dir_path}"
                        pull_results = run_command(adb_pull_command)

                        # Check if --delete flag is used before deleting
                        if args.delete:
                            if "file pulled" in pull_results[0] or "bytes in" in pull_results[0]:
                                adb_delete_command = f"adb shell rm {CONFIG[task]['source_path']}/{file}"
                                run_command(adb_delete_command)

                    overall_progress.update(file_sizes[file])

if __name__ == "__main__":
    main()
