
# QPull - Oculus File Management Script

## Overview
QPul is a Python script designed to manage files on an Oculus device. It allows for efficient transfer and deletion of screen recordings and screenshots from the Oculus to your computer.

## Features
- Pull screen recordings and screenshots from Oculus device.
- Organize files into date-based subdirectories.
- Option to delete files from the Oculus device after transfer.
- Handle recordings, screenshots, or both simultaneously.

## Requirements
- Python 3
- ADB (Android Debug Bridge) installed and configured.
- tqdm and humanize Python packages.

## Installation
1. Clone the repository or download the script.
2. Ensure Python 3 is installed on your system.
3. Install the required Python packages:
   ```bash
   pip install tqdm humanize
   ```
4. Connect your Oculus device via USB and enable file transfer / developer mode.

## Usage
Run the script using Python, with the desired flags:
- `--delete`: Delete files from the Oculus device after transfer.
- `--recordings` or `-r`: Process only screen recordings.
- `--shots` or `-s`: Process only screenshots.
- `--all` or `-a`: Process both recordings and screenshots.

Example:
```bash
python qpull.py --all --delete
```

## Configuration
Modify the `CONFIG` dictionary in the script to set the source and destination paths for recordings and screenshots.

## License
This project is licensed under the MIT License.

## Disclaimer
This script is not officially affiliated with Oculus or its products. Use at your own risk.
