import os
import time
from datetime import datetime
import pywintypes
import win32file
import win32con

def change_folder_times(folder_path, dt):
    # Convert to pywintypes.Time
    win_time = pywintypes.Time(dt.timestamp())
    # Open the folder handle
    handle = win32file.CreateFile(
        folder_path,
        win32con.GENERIC_WRITE,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG_BACKUP_SEMANTICS,
        None
    )
    # Set creation and last write (modified) times
    win32file.SetFileTime(handle, win_time, None, win_time)
    handle.Close()

def get_file_stats(file_path):
    stats = os.stat(file_path)
    print(f'File Size: {stats.st_size} bytes')
    print(f'Last Modified: {time.ctime(stats.st_mtime)}')
    print(f'Last Accessed: {time.ctime(stats.st_atime)}')
    print(f'Creation Time: {time.ctime(stats.st_ctime)}')

folder_name = input("Nome della cartella: ")
if not folder_name:
    quit("Bye bye")

print("Imposta la data/ora desiderata:")
year    = int(input("Anno: \t"))
month   = int(input("Mese: \t"))
day     = int(input("Giorno: "))
hour    = int(input("Ora: \t"))
minute  = int(input("Minuto: "))
second  = int(input("Secondi:"))

dt = datetime(year, month, day, hour, minute, second)
change_folder_times(folder_name, dt)
get_file_stats(folder_name)
print("Fatto!")