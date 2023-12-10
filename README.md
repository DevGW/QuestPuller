
# QPull - Oculus File Management Script

## Overview
QPull is a Python script designed to manage files on an Oculus device. It allows for efficient transfer and deletion of screen recordings and screenshots from the Oculus to your computer.

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
4. Connect your Oculus device via USB and enable file transfer mode.

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

## Setup Script and Wrapper Installation
The repository includes a setup script (`setup.py`) to simplify the installation and configuration of the `qpull` script.

### Using the Setup Script
1. Run the `setup.py` script in the root of the project directory.
2. The script will:
   - Create a Python virtual environment if it doesn't exist.
   - Install required Python packages from `requirements.txt`.
   - Create or update the `qpull` wrapper script in the specified location (or current working directory if not specified).
   - Set execute permissions for the `qpull` wrapper (Unix-based systems).

Example:
```bash
python setup.py /path/to/destination
```

### Using the Wrapper
Once the setup script has been executed, you can use the `qpull` wrapper script to run the qpull Python script without manually activating the virtual environment. This is particularly useful on Unix-based systems. On Windows, you can directly run the `qpull.py` script from the virtual environment.

Example (Unix-based systems):
```bash
/path/to/destination/qpull --all --delete
```

Example (Windows):
```bash
/path/to/virtualenv/Scripts/python /path/to/qpull.py --all --delete
```

Note: If you move the location of the project directory, you will need to run the setup script again to update the `qpull` wrapper.
