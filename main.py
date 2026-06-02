import os
import sys
from datetime import datetime


def prompt_path() -> str:
    while True:
        path = input("Enter a file or directory path: ").strip()
        if not path:
            print("Path cannot be empty. Please try again.")
            continue

        path = os.path.expanduser(path)
        path = os.path.abspath(path)

        if not os.path.exists(path):
            print(f"Path does not exist: {path}")
            continue

        return path


def prompt_int(label: str, min_value: int, max_value: int) -> int:
    while True:
        value = input(f"Enter {label} ({min_value}-{max_value}): ").strip()
        if not value:
            print("Input cannot be empty. Please try again.")
            continue
        if not value.isdigit():
            print("Please enter a whole number.")
            continue

        value_int = int(value)
        if value_int < min_value or value_int > max_value:
            print(f"{label} must be between {min_value} and {max_value}.")
            continue

        return value_int


def prompt_datetime() -> datetime:
    print("Enter the target date and time:")
    year = prompt_int("year", 1, 9999)
    month = prompt_int("month", 1, 12)
    day = prompt_int("day", 1, 31)
    hour = prompt_int("hour", 0, 23)
    minute = prompt_int("minute", 0, 59)
    second = prompt_int("second", 0, 59)

    try:
        return datetime(year, month, day, hour, minute, second)
    except ValueError as exc:
        print(f"Invalid date: {exc}")
        return prompt_datetime()


def set_modification_time(path: str, timestamp: float) -> None:
    os.utime(path, (timestamp, timestamp))


def set_creation_time_windows(path: str, dt: datetime) -> bool:
    try:
        import pywintypes
        import win32file
        import win32con
    except ImportError:
        return False

    file_handle = None
    flags = win32con.FILE_FLAG_BACKUP_SEMANTICS
    try:
        file_handle = win32file.CreateFile(
            path,
            win32con.GENERIC_WRITE,
            win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
            None,
            win32con.OPEN_EXISTING,
            flags,
            None,
        )
        win_time = pywintypes.Time(dt)
        win32file.SetFileTime(file_handle, win_time, win_time, win_time)
        return True
    except Exception:
        return False
    finally:
        if file_handle is not None and file_handle != win32file.INVALID_HANDLE_VALUE:
            file_handle.Close()


def print_summary(path: str, dt: datetime, creation_set: bool) -> None:
    print("\nMetadata update completed.")
    print(f"Target path: {path}")
    print(f"New date/time: {dt.isoformat(sep=' ')}")
    print("Modification time updated.")
    if creation_set:
        print("Creation time updated.")
    else:
        print("Creation time could not be updated on this platform or pywin32 is not installed.")


def main() -> None:
    if not sys.stdin.isatty() or not sys.stdout.isatty():
        print("This script is designed to be run in a terminal.")

    target_path = prompt_path()
    target_datetime = prompt_datetime()
    timestamp = target_datetime.timestamp()

    set_modification_time(target_path, timestamp)

    creation_set = False
    if os.name == "nt":
        creation_set = set_creation_time_windows(target_path, target_datetime)

    print_summary(target_path, target_datetime, creation_set)


if __name__ == "__main__":
    main()
