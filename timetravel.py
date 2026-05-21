# Get command-line filename parameter instead of prompting
import argparse
import os
import sys
import time
from datetime import datetime
#, timezone, timedelta
import pywintypes
import win32file
import win32con


def change_creation_time(file_path, new_time):
    # Convert the new time to the correct format
    new_time = time.mktime(new_time.timetuple())
    new_time = pywintypes.Time(new_time)

    # Open the file in write modedoc09333620250530102743.pdf
    handle = win32file.CreateFile(
        file_path, win32con.GENERIC_WRITE, 0, None, win32con.OPEN_EXISTING, 0, None
    )

    # Change the creation time of the file
    win32file.SetFileTime(handle, new_time, new_time, new_time)

    # Close the file handle
    handle.Close()

def get_file_stats(file_path):
    stats = os.stat(file_path)

    print(f'File Size: {stats.st_size} bytes')
    print(f'Last Modified: {time.ctime(stats.st_mtime)}')
    print(f'Last Accessed: {time.ctime(stats.st_atime)}')
    print(f'Creation Time: {time.ctime(stats.st_ctime)}')
    print(f'File Mode: {stats.st_mode}')
    print(f'File Inode: {stats.st_ino}')

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Change file creation time")
parser.add_argument("file", nargs="?", help="Path to the file to modify")
args = parser.parse_args()
file_name = args.file

if not file_name:
    sys.exit("Please provide a file path. Usage: python timetravel.py <file>")

if not os.path.exists(file_name):
    sys.exit(f"File not found: {file_name}")


year    = int(input("Anno: \t"))
month   = int(input("Mese: \t"))
day     = int(input("Giorno: "))
hour    = int(input("Ora: \t"))
minute  = int(input("Minuto: "))
second  = int(input("Secondi:"))

new_time = datetime(year, month, day, hour, minute, second)

# Convert the datetime object to a different timezone
#new_time = new_time.astimezone(timezone(timedelta(hours=1)))

# Now you can convert the datetime object to a pywintypes.datetime object
new_time = pywintypes.Time(new_time.timestamp())


change_creation_time(file_name, new_time)
get_file_stats(file_name)

print("Fatto!")