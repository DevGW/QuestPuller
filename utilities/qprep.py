#!/usr/bin/env python3
import subprocess

def run_adb_commands():
    commands = [
        "adb shell setprop debug.oculus.capture.width 1920", # default is 1024
        "adb shell setprop debug.oculus.capture.height 1080", # default is 1024
        "adb shell setprop debug.oculus.capture.bitrate 10000000", # default is 50000000
        "adb shell setprop debug.oculus.capture.fps 60", # default is 30
        "adb shell setprop debug.oculus.foveation.level 0" # default is 2
    ]

    for command in commands:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()

        if process.returncode != 0:
            print(f"Error executing command: {command}")
            print(f"Error message: {stderr.decode().strip()}")
        else:
            print(f"Successfully executed command: {command}")
            print(stdout.decode().strip())

if __name__ == "__main__":
    run_adb_commands()
